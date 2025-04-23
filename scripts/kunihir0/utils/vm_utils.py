#!/usr/bin/env python3

"""
Safe utility functions for VM operations used by the UMK cleanup tools.

This module follows the ULTMOS coding standards:
- Uses pathlib instead of os module
- Uses subprocess for command execution via safe_command_utils
- Includes type hints
- Has proper exception handling using the centralized logger
- Prioritizes file-based VM detection over runtime checks
"""

import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

# Import safe utilities and logger
from .logger import default_logger as log
from .safe_command_utils import (
    run_command_with_output,
    run_virsh_command as safe_run_virsh_command,
    check_command_exists
)
from .safe_file_utils import (
    ensure_directory_exists,
    write_file_text,
    is_valid_file,
    is_valid_directory,
    read_file_text,
    delete_file
)
from .config_utils import BlobData # Keep config_utils for BlobData

class VirtualMachine:
    """Class representing a detected virtual machine."""

    def __init__(
        self,
        name: str,
        state: str = "unknown",
        script_path: Optional[Path] = None, # Added script path
        xml_path: Optional[Path] = None,
        disk_paths: Optional[List[Path]] = None
    ):
        """Initialize a VM object.

        Args:
            name: Name of the VM (often derived from script name)
            state: Current state (e.g., defined, running, shut off)
            script_path: Path to the VM boot script (.sh)
            xml_path: Path to the VM XML file if known
            disk_paths: List of VM disk paths if known
        """
        self.name = name
        self.state = state
        self.script_path = script_path # Store script path
        self.xml_path = xml_path
        self.disk_paths = disk_paths if disk_paths else []

    def __str__(self) -> str:
        """String representation of the VM."""
        script_info = f" (Script: {self.script_path.name})" if self.script_path else ""
        return f"{self.name}{script_info} ({self.state})"

# --- Helper Functions (Keep QEMU process detection for state checking) ---
# (QEMU process detection helpers _find_qemu_processes and _extract_info_from_qemu_cmdline remain unchanged for now)
# --- Helper Functions for QEMU Process Detection ---

def _find_qemu_processes() -> List[Dict[str, Any]]:
    """Find running QEMU processes and parse their command lines."""
    processes = []
    try:
        # Use pgrep to find PIDs of qemu processes
        # '-a' includes command line, '-f' matches full command line
        pgrep_cmd = ["pgrep", "-af", "qemu-system-x86_64"]
        # Use safe command runner
        success, output, stderr = run_command_with_output(pgrep_cmd, quiet=True)

        if not success or not output:
            if stderr and "command not found" in stderr.lower():
                 log.warning("pgrep command not found. Cannot find QEMU processes via pgrep.")
            elif stderr:
                 log.warning(f"pgrep command failed: {stderr}")
            # Could also try ps aux | grep qemu as a fallback if pgrep fails or isn't available
            # For simplicity, we'll stick with pgrep for now.
            return processes

        lines = output.strip().split('\n')
        for line in lines:
            parts = line.split(' ', 1) # Split PID from command line
            if len(parts) == 2:
                pid_str, cmdline = parts
                try:
                    pid = int(pid_str)
                    # Basic check to avoid matching the pgrep command itself
                    if "pgrep -af qemu-system-x86_64" not in cmdline:
                         processes.append({"pid": pid, "cmdline": cmdline})
                except ValueError:
                    # Ignore lines where PID isn't an integer
                    log.debug(f"Ignoring non-integer PID in pgrep output: {pid_str}")
                    continue
    except FileNotFoundError:
         # This might happen if pgrep isn't installed
         log.warning("pgrep command not found. Cannot find QEMU processes via pgrep.")
    except Exception as e:
        log.exception("Unexpected error finding QEMU processes", e)
    return processes

def _extract_info_from_qemu_cmdline(cmdline: str, pid: Optional[int] = None) -> Dict[str, Any]:
    """Extract potential VM name and disk paths from QEMU command line."""
    info = {"name": None, "disk_paths": [], "is_macos_likely": False}

    # Simple name extraction (look for -name argument)
    # Handles names with commas like 'guest=name,debug-threads=on'
    name_match = re.search(r'-name\s+([^,\s]+(?:,[^,\s]+)*)', cmdline)
    if name_match:
         # Further refine name if it includes options like 'guest='
         name_part = name_match.group(1)
         if name_part.startswith("guest="):
             # Extract 'name' from 'guest=name,debug...'
             guest_parts = name_part.split(',')
             name_val = guest_parts[0].split('=', 1)
             if len(name_val) == 2:
                 info["name"] = name_val[1]
         elif name_part.startswith("process="):
             # Handle cases like -name process=foo,debug-threads=on
             process_parts = name_part.split(',')
             name_val = process_parts[0].split('=', 1)
             if len(name_val) == 2:
                 info["name"] = name_val[1]
         else:
             # Use the first part before comma if it's not guest= or process=
             info["name"] = name_part.split(',')[0]


    # Extract disk paths (look for -drive file=...)
    # More robust regex to handle different quoting and formats
    drive_pattern = r"-drive\s+(?:[^=\s]+=)*file=[\'\"`]?([^\'\"`\s]+)[\'\"`]?"
    disk_matches = re.findall(drive_pattern, cmdline)
    for path_str in disk_matches:
        # Basic filtering of non-disk files
        if not any(ext in path_str.lower() for ext in ['.iso', '.rom', '.fd']):
             try:
                 # Attempt to resolve, but don't fail if it doesn't exist yet
                 p = Path(path_str)
                 info["disk_paths"].append(p)
                 # Check if common macOS disk names are present
                 if p.name in ["OpenCore.qcow2", "BaseSystem.img", "HDD.qcow2"]:
                     info["is_macos_likely"] = True
             except ValueError as e: # More specific exception for Path errors
                 log.warning(f"Could not parse potential disk path: {path_str}: {e}")
             except Exception as e: # Catch other unexpected errors
                 log.exception(f"Unexpected error parsing disk path {path_str}", e)


    # Check for other macOS indicators in command line
    macos_indicators_cmd = [
        "-cpu Penryn",
        "-cpu Haswell",
        "OVMF_CODE.fd",
        "OpenCore.qcow2", # Check again in case regex missed it
        "vmxnet3",
        "usb-ehci",
        "ich9-intel-hda",
        "fw_cfg name=opt/ovmf/X-PciMmio64Mb", # Common OVMF setting
    ]
    if any(indicator in cmdline for indicator in macos_indicators_cmd):
        info["is_macos_likely"] = True

    # If no name found via -name, try to infer from disk path
    if not info["name"] and info["disk_paths"]:
        # Try to find a name based on a qcow2 file, preferring HDD.qcow2
        hhd_disk = next((d for d in info["disk_paths"] if d.name == "HDD.qcow2"), None)
        if hhd_disk:
             # Infer name from parent directory if possible, or use a default
             try:
                 parent_dir_name = hhd_disk.parent.name
                 if parent_dir_name and parent_dir_name != '.':
                     info["name"] = f"qemu_{parent_dir_name}"
                 else:
                     info["name"] = "qemu_macos_vm" # Default name
             except Exception as e:
                 log.exception(f"Error inferring VM name from disk path {hhd_disk}", e)
                 info["name"] = "qemu_macos_vm" # Fallback on error
        else:
             # Use the name of the first qcow2 file found
             first_qcow2 = next((d for d in info["disk_paths"] if d.suffix == '.qcow2'), None)
             if first_qcow2:
                 info["name"] = f"qemu_{first_qcow2.stem}"
             else:
                 # Fallback if no suitable disk name found
                 # Use PID and timestamp for uniqueness, avoiding os module
                 pid_str = str(pid) if pid is not None else "unknown"
                 timestamp_str = str(int(time.time()))[-6:] # Last 6 digits of timestamp
                 info["name"] = f"qemu_vm_pid{pid_str}_{timestamp_str}"


    return info

# --- End Helper Functions ---


def _get_vm_state(vm_name: str) -> str:
    """Check virsh and QEMU processes to determine runtime state."""
    state = "defined" # Default state if found via files but not running

    # 1. Check Libvirt state
    if check_command_exists("virsh", quiet=True):
        success, output, stderr = safe_run_virsh_command(["domstate", vm_name], quiet=True) # Use safe alias
        if success:
            virsh_state = output.strip()
            if virsh_state == "running":
                return "running (libvirt)"
            elif virsh_state == "shut off":
                state = "shut off (libvirt)"
            elif virsh_state: # paused, pmsuspended, etc.
                state = f"{virsh_state} (libvirt)"
        else: # Command failed or domain not found
            stderr_lower = stderr.lower()
            if f"domain '{vm_name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                 log.debug(f"VM '{vm_name}' not found via virsh (domstate).")
                 # Keep state as "defined" or whatever the default is before this check
            elif "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 log.warning(f"Permission error getting state for VM '{vm_name}'. Check libvirt access permissions (e.g., group membership, polkit) or try running the script with sudo.")
                 # Keep state as "defined" but log the warning
            elif stderr: # Log other errors
                 log.warning(f"Could not get libvirt state for VM '{vm_name}': {stderr}")
            # If not found or permission error, proceed to check QEMU processes

    # 2. Check QEMU processes if not found running or accessible in libvirt
    if "running" not in state:
        try:
            qemu_processes = _find_qemu_processes()
            for proc in qemu_processes:
                pid = proc.get("pid")
                cmdline = proc.get("cmdline", "")
                proc_info = _extract_info_from_qemu_cmdline(cmdline, pid)
                extracted_name = proc_info.get("name")
                # Check if process name matches (case-insensitive might be better)
                if extracted_name and extracted_name.lower() == vm_name.lower():
                    log.debug(f"Found running QEMU process for VM '{vm_name}' (PID: {pid})")
                    return "running (QEMU process)"
        except Exception as e:
            log.exception(f"Error checking QEMU processes for VM state '{vm_name}'", e)

    return state


def find_macos_vms() -> List[VirtualMachine]:
    """
    Find macOS VMs primarily by looking for configuration files
    (.sh scripts and associated blobs) in the project directory.
    Optionally updates state based on runtime checks (virsh/QEMU process).
    """
    vms: Dict[str, VirtualMachine] = {} # Use dict to deduplicate by name (script name)
    log.info("Searching for VM configurations based on .sh scripts and blobs...")

    try:
        project_root = Path(__file__).resolve().parents[3] # Correct index for project root
        blobs_user_dir = project_root / "blobs" / "user"

        # Scan for potential boot scripts in the project root
        for script_path in project_root.glob('*.sh'):
            if not is_valid_file(script_path, quiet=True):
                continue

            vm_name_from_script = script_path.stem # e.g., "boot" from "boot.sh"
            log.debug(f"Found potential script: {script_path.name}, potential VM name: {vm_name_from_script}")

            # Check for corresponding user blobs as confirmation
            # Check both ./blobs/ and ./blobs/user/ for the config blob
            cfg_blob_path_user = blobs_user_dir / "USR_CFG.apb"
            cfg_blob_path_root = project_root / "blobs" / "USR_CFG.apb" # Check root blobs dir too
            vm_name_blob_path = blobs_user_dir / "USR_VM_NAME.apb" # Or check VM name blob

            is_confirmed_vm = False
            vm_name = vm_name_from_script # Default name
            cfg_content = None
            cfg_content_user = None
            cfg_content_root = None

            # Try reading from ./blobs/user/ first
            log.debug(f"Checking blob path (user): {cfg_blob_path_user}")
            if is_valid_file(cfg_blob_path_user, quiet=True):
                 cfg_content_user = read_file_text(cfg_blob_path_user, quiet=True)
                 log.debug(f"Content (user): '{cfg_content_user}'")
                 if cfg_content_user:
                     cfg_content = cfg_content_user # Prioritize user blob content
                     log.debug(f"Using CFG blob content from user dir: {cfg_blob_path_user}")

            # If not found or empty in user dir, try reading from ./blobs/
            log.debug(f"Checking blob path (root): {cfg_blob_path_root}")
            if not cfg_content and is_valid_file(cfg_blob_path_root, quiet=True):
                 cfg_content_root = read_file_text(cfg_blob_path_root, quiet=True)
                 log.debug(f"Content (root): '{cfg_content_root}'")
                 if cfg_content_root:
                     cfg_content = cfg_content_root # Use root blob content as fallback
                     log.debug(f"Using CFG blob content from root blobs dir: {cfg_blob_path_root}")

            # Now check if content matches script name
            log.debug(f"Comparing blob content '{cfg_content.strip() if cfg_content else None}' with script name '{script_path.name}'")
            if cfg_content and cfg_content.strip() == script_path.name:
                is_confirmed_vm = True
                log.debug(f"CONFIRMED VM '{vm_name}' via CFG blob matching script name '{script_path.name}'.")
                # Look for VM name in blob files - this is crucial for matching with libvirt
                # Check both VM_NAME and TARGET_VM_NAME blobs
                vm_name_blob_path = blobs_user_dir / "USR_VM_NAME.apb"
                target_vm_name_blob_path = blobs_user_dir / "USR_TARGET_VM_NAME.apb"
                
                if is_valid_file(vm_name_blob_path, quiet=True):
                     name_content = read_file_text(vm_name_blob_path, quiet=True)
                     if name_content:
                          vm_name = name_content.strip()
                          log.debug(f"Using VM name from USR_VM_NAME.apb: {vm_name}")
                elif is_valid_file(target_vm_name_blob_path, quiet=True):
                     name_content = read_file_text(target_vm_name_blob_path, quiet=True)
                     if name_content:
                          vm_name = name_content.strip()
                          log.debug(f"Using VM name from USR_TARGET_VM_NAME.apb: {vm_name}")


            # If confirmed, create VM object and determine state
            if is_confirmed_vm and vm_name not in vms:
                 state = _get_vm_state(vm_name) # Check runtime state
                 # Extract disk paths (can reuse existing logic or adapt)
                 # For simplicity, we might skip detailed disk path extraction here
                 # or try reading USR_HDD_PATH.apb
                 disk_paths_set: Set[Path] = set() # Use a set to avoid duplicates
                 # Attempt to add disk from HDD blob
                 hdd_path_blob = blobs_user_dir / "USR_HDD_PATH.apb"
                 hdd_path_str = read_file_text(hdd_path_blob, quiet=True)
                 if hdd_path_str:
                      try:
                           # Handle $VM_PATH replacement if necessary
                           if "$VM_PATH" in hdd_path_str:
                                hdd_path_str = hdd_path_str.replace("$VM_PATH", str(project_root))
                           hdd_path = Path(hdd_path_str)
                           if is_valid_file(hdd_path, quiet=True): # Check if path from blob is valid
                                disk_paths_set.add(hdd_path)
                                log.debug(f"Added disk from blob: {hdd_path}")
                           else:
                                log.warning(f"Disk path from blob is invalid: {hdd_path}")
                      except Exception as e:
                           log.warning(f"Could not parse disk path from blob {hdd_path_blob}: {e}")

                 # Explicitly check for BaseSystem.img/.dmg in project root
                 basesystem_img = project_root / "BaseSystem.img"
                 basesystem_dmg = project_root / "BaseSystem.dmg"
                 if is_valid_file(basesystem_img, quiet=True):
                      disk_paths_set.add(basesystem_img)
                      log.debug(f"Added disk: {basesystem_img}")
                      
                      # Also check for associated HDD.qcow2 in the same directory
                      hdd_qcow2 = basesystem_img.parent / "HDD.qcow2"
                      if is_valid_file(hdd_qcow2, quiet=True):
                           disk_paths_set.add(hdd_qcow2)
                           log.debug(f"Added associated disk: {hdd_qcow2}")
                 elif is_valid_file(basesystem_dmg, quiet=True): # Check for DMG as fallback
                      disk_paths_set.add(basesystem_dmg)
                      log.debug(f"Added disk: {basesystem_dmg}")
                      
                      # Also check for associated HDD.qcow2 in the same directory
                      hdd_qcow2 = basesystem_dmg.parent / "HDD.qcow2"
                      if is_valid_file(hdd_qcow2, quiet=True):
                           disk_paths_set.add(hdd_qcow2)
                           log.debug(f"Added associated disk: {hdd_qcow2}")


                 vms[vm_name] = VirtualMachine(
                     name=vm_name,
                     state=state,
                     script_path=script_path,
                     xml_path=project_root / f"{vm_name}.xml", # Assume XML might exist
                     disk_paths=sorted(list(disk_paths_set)) # Convert set to sorted list
                 )
                 log.info(f"Detected VM: {vms[vm_name]} with disks: {[p.name for p in vms[vm_name].disk_paths]}")

    except Exception as e:
        log.exception("Unexpected error during file-based VM discovery", e)

    return list(vms.values())


def find_vm_by_name(vm_name: str) -> Optional[VirtualMachine]:
    """
    Find a specific VM primarily by checking for its configuration files
    (<vm_name>.sh) and associated blobs. Updates state from runtime checks.
    """
    log.debug(f"Attempting to find VM '{vm_name}' by file configuration...")
    try:
        project_root = Path(__file__).resolve().parents[3] # Correct index for project root
        script_path = project_root / f"{vm_name}.sh"

        # Primary check: Does the script file exist?
        if is_valid_file(script_path, quiet=False): # Log warning if not found
            log.debug(f"Found script file for VM '{vm_name}': {script_path}")

            # Determine state and check for XML
            state = _get_vm_state(vm_name)
            xml_path = extract_xml_path(vm_name) # Checks libvirt paths and local

            # Check for custom VM name in blobs
            blobs_user_dir = project_root / "blobs" / "user"
            vm_name_orig = vm_name  # Store the original name for reference
            
            # Look for VM name in blob files
            vm_name_blob_path = blobs_user_dir / "USR_VM_NAME.apb"
            target_vm_name_blob_path = blobs_user_dir / "USR_TARGET_VM_NAME.apb"
            
            try:
                if is_valid_file(vm_name_blob_path, quiet=True):
                    name_content = read_file_text(vm_name_blob_path, quiet=True)
                    if name_content:
                        vm_name = name_content.strip()
                        log.debug(f"Using VM name from USR_VM_NAME.apb: {vm_name} (was: {vm_name_orig})")
                elif is_valid_file(target_vm_name_blob_path, quiet=True):
                    name_content = read_file_text(target_vm_name_blob_path, quiet=True)
                    if name_content:
                        vm_name = name_content.strip()
                        log.debug(f"Using VM name from USR_TARGET_VM_NAME.apb: {vm_name} (was: {vm_name_orig})")
            except Exception as e:
                log.warning(f"Error reading VM name blobs for {vm_name}: {e}")
                
            # Attempt to get disk path from blobs (best effort)
            disk_paths = []
            try:
                hdd_path_blob = blobs_user_dir / "USR_HDD_PATH.apb"
                hdd_path_str = read_file_text(hdd_path_blob, quiet=True)
                if hdd_path_str:
                     if "$VM_PATH" in hdd_path_str:
                          hdd_path_str = hdd_path_str.replace("$VM_PATH", str(project_root))
                     disk_paths.append(Path(hdd_path_str))
            except Exception as e:
                 log.warning(f"Could not parse disk path from blob for {vm_name}: {e}")
                 
            # Check for BaseSystem.img/.dmg and associated HDD.qcow2 files
            try:
                basesystem_img = project_root / "BaseSystem.img"
                basesystem_dmg = project_root / "BaseSystem.dmg"
                if is_valid_file(basesystem_img, quiet=True):
                    if basesystem_img not in disk_paths:
                        disk_paths.append(basesystem_img)
                        log.debug(f"Added disk: {basesystem_img}")
                    
                    # Check for associated HDD.qcow2
                    hdd_qcow2 = basesystem_img.parent / "HDD.qcow2"
                    if is_valid_file(hdd_qcow2, quiet=True) and hdd_qcow2 not in disk_paths:
                        disk_paths.append(hdd_qcow2)
                        log.debug(f"Added associated disk: {hdd_qcow2}")
                elif is_valid_file(basesystem_dmg, quiet=True):
                    if basesystem_dmg not in disk_paths:
                        disk_paths.append(basesystem_dmg)
                        log.debug(f"Added disk: {basesystem_dmg}")
                    
                    # Check for associated HDD.qcow2
                    hdd_qcow2 = basesystem_dmg.parent / "HDD.qcow2"
                    if is_valid_file(hdd_qcow2, quiet=True) and hdd_qcow2 not in disk_paths:
                        disk_paths.append(hdd_qcow2)
                        log.debug(f"Added associated disk: {hdd_qcow2}")
            except Exception as e:
                log.warning(f"Error checking for BaseSystem and HDD files: {e}")

            # Create the VM object
            found_vm = VirtualMachine(
                name=vm_name,
                state=state,
                script_path=script_path,
                xml_path=xml_path,
                disk_paths=disk_paths
            )
            log.info(f"Found VM by name '{vm_name}' via file configuration: {found_vm}")
            return found_vm
        else:
            # Script file itself wasn't found
            log.info(f"VM script file '{script_path.name}' not found.")
            return None

    except Exception as e:
        log.exception(f"Error finding VM by name '{vm_name}' via files", e)
        return None


def is_macos_vm(xml_content: str) -> bool:
    """Check if XML content is for a macOS VM based on libvirt XML."""
    # (Logic remains the same as before)
    macos_indicators = [
        "<type arch='x86_64' machine='q35'>hvm</type>",
        "<boot dev='pflash'",
        "OpenCore.qcow2",
        "OVMF_CODE.fd",
        "OVMF_VARS.fd",
        "macOS",
        "Mac OS X"
    ]
    os_match = re.search(r'<os>.*?<type.*?>(hvm)</type>.*?</os>', xml_content, re.DOTALL)
    if not os_match or os_match.group(1) != 'hvm':
        return False
    if "<loader" not in xml_content or "<nvram" not in xml_content:
        pass # Allow for now
    for indicator in macos_indicators:
        if indicator in ["macOS", "Mac OS X"]:
             if re.search(indicator, xml_content, re.IGNORECASE):
                 return True
        elif indicator in xml_content:
            return True
    return False


def extract_disk_paths(xml_content: str) -> List[Path]:
    """Extract disk paths from VM XML content."""
    # (Logic remains the same as before)
    disk_paths: List[Path] = []
    pattern = r'<source file=[\'"]([^\'"]+)[\'"]'
    matches = re.findall(pattern, xml_content)
    for match in matches:
        if any(ext in match.lower() for ext in [".iso", ".rom", ".fd"]):
            continue
        try:
            disk_paths.append(Path(match))
        except ValueError as e:
             log.warning(f"Could not parse potential disk path from XML: {match} ({e})")
        except Exception as e:
             log.exception(f"Unexpected error parsing disk path from XML: {match}", e)
    return disk_paths


def extract_xml_path(vm_name: str) -> Optional[Path]:
    """Find the XML file path for a VM defined in libvirt."""
    # (Logic remains the same as before, using safe utils)
    xml_locations = [
        Path("/etc/libvirt/qemu"),
        Path("/var/lib/libvirt/qemu"),
        Path.home() / ".config/libvirt/qemu",
        Path.home() / ".local/share/libvirt/qemu"
    ]
    for location in xml_locations:
        try:
            if is_valid_directory(location, quiet=True):
                xml_path = location / f"{vm_name}.xml"
                if is_valid_file(xml_path, quiet=True):
                    return xml_path
        except PermissionError:
             log.debug(f"Permission denied checking libvirt XML location: {location}")
        except Exception as e:
            log.exception(f"Error checking libvirt XML location {location}", e)
    return None


def find_vms_from_blob_data(blob_data: BlobData) -> List[VirtualMachine]:
    """
    DEPRECATED: Use find_macos_vms or find_vm_by_name instead.
    Find VMs using information primarily from blob files.
    """
    log.warning("find_vms_from_blob_data is deprecated. Use find_macos_vms or find_vm_by_name.")
    vms: List[VirtualMachine] = []
    if blob_data.vm_name:
        vm = find_vm_by_name(blob_data.vm_name) # Uses new file-based logic
        if vm:
            vms.append(vm)
    if not vms:
        vms = find_macos_vms() # Uses new file-based logic
    return vms


def shutdown_vm(vm_name: str, force: bool = False, timeout: int = 60, dry_run: bool = False) -> bool: # Add dry_run
    """Safely shutdown a VM managed by libvirt."""
    log.info(f"Initiating shutdown sequence for '{vm_name}'... (Dry Run: {dry_run})")
    if not check_command_exists("virsh", quiet=True):
        log.warning("'virsh' command not found. Cannot shutdown VM.")
        return False
    try:
        success_state, state_output, stderr_state = safe_run_virsh_command( # Use safe alias
            ["domstate", vm_name], quiet=True
        )
        if not success_state:
            stderr_lower = stderr_state.lower()
            if f"domain '{vm_name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                 log.info(f"VM '{vm_name}' not found via virsh. Assuming not running.")
                 return True
            elif "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 log.warning(f"Permission error getting state for VM '{vm_name}'. Check libvirt access permissions.")
                 return False # Cannot determine state, assume failure for shutdown
            else:
                 log.error(f"Could not get state for VM '{vm_name}': {stderr_state}")
                 return False
        state = state_output.strip()
        if state != "running":
            log.info(f"VM '{vm_name}' is not running (state: {state}).")
            return True

        # --- Shutdown/Destroy Logic ---
        action_cmd = ["destroy", vm_name] if force else ["shutdown", vm_name]
        action_name = "force destroy" if force else "graceful shutdown"
        log.info(f"Attempting {action_name} for VM '{vm_name}'...")

        success_action = True # Assume success for dry run
        stderr_action = ""
        if not dry_run:
            success_action, _, stderr_action = safe_run_virsh_command(action_cmd, quiet=False)
        else:
            log.info(f"[Dry Run] Would execute: virsh {' '.join(action_cmd)}")

        if not success_action:
            stderr_lower = stderr_action.lower()
            if "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 log.error(f"Permission error attempting {action_name} for VM '{vm_name}'. Check libvirt permissions.")
            # else: Error already logged by safe_run_virsh_command (quiet=False)
            # If force=True, we return the failure status here
            if force:
                return False
            # If force=False (graceful shutdown failed), we still might need to wait/force later
            log.error(f"Error initiating graceful shutdown for VM '{vm_name}': {stderr_action}")
            return False # Fail graceful shutdown if initial command fails

        # If graceful shutdown initiated successfully (force=False and success_action=True)
        if not force:
            log.info(f"Waiting up to {timeout} seconds for VM '{vm_name}' to shut down...")
            start_time = time.time()
            while time.time() - start_time < timeout:
                wait_success, wait_state, wait_stderr = safe_run_virsh_command( # Use safe alias
                    ["domstate", vm_name], quiet=True
                )
                if not wait_success:
                    # Log permission error specifically if it happens during wait
                    stderr_lower = wait_stderr.lower()
                    if "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                         log.error(f"Permission error getting VM state while waiting for shutdown. Check libvirt permissions.")
                    else:
                         log.error(f"Error getting VM state while waiting for shutdown: {wait_stderr}")
                    # Continue waiting despite error? Or break? Let's break to avoid spamming logs.
                    break
                else:
                    current_state = wait_state.strip()
                    if current_state != "running":
                        log.success(f"VM '{vm_name}' shut down successfully (state: {current_state}).")
                        return True
                time.sleep(2)
            # If loop finishes, timeout occurred
            log.warning(f"Graceful shutdown of VM '{vm_name}' timed out after {timeout}s, forcing destroy...")
            success_destroy_timeout = True # Assume success for dry run
            stderr_destroy_timeout = ""
            if not dry_run:
                success_destroy_timeout, _, stderr_destroy_timeout = safe_run_virsh_command( # Use safe alias
                    ["destroy", vm_name], quiet=False
                )
            else:
                 log.info(f"[Dry Run] Would execute: virsh destroy {vm_name}")

            if not success_destroy_timeout:
                 stderr_lower = stderr_destroy_timeout.lower()
                 if "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                      log.error(f"Permission error forcing destroy on VM '{vm_name}' after timeout. Check libvirt permissions.")
                 # else: Error logged by safe_run_virsh_command
            return success_destroy_timeout
        # If force=True and initial destroy succeeded
        elif force and success_action:
             return True
        # Should not be reached if logic is correct, but return False as a fallback
        return False
    except Exception as e:
        log.exception(f"An unexpected error occurred during VM shutdown for '{vm_name}'", e)
        return False


def undefine_vm(vm_name: str, remove_storage: bool = False, dry_run: bool = False) -> bool: # Add dry_run
    """Undefine a VM from libvirt."""
    log.info(f"Attempting to undefine VM '{vm_name}'... (Dry Run: {dry_run})")
    command = ["undefine", vm_name]
    if remove_storage:
        log.warning(f"--remove-all-storage requested for {vm_name}. Ensure storage pools are correctly configured.")
        command.append("--remove-all-storage")
    if not check_command_exists("virsh", quiet=True):
        log.warning("'virsh' command not found. Cannot undefine VM.")
        return False
    try:
        success = True # Assume success for dry run
        stderr = ""
        if not dry_run:
            success, _, stderr = safe_run_virsh_command(command, quiet=False)
        else:
            log.info(f"[Dry Run] Would execute: virsh {' '.join(command)}")

        if not success:
            stderr_lower = stderr.lower()
            if f"domain '{vm_name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                 log.info(f"VM '{vm_name}' not found or already undefined.")
                 return True # Treat as success if not found
            elif "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 log.error(f"Permission error undefining VM '{vm_name}'. Check libvirt permissions.")
                 return False # Operation failed due to permissions
            # else: Generic error logged by safe_run_virsh_command
            return False # Operation failed for other reason
        log.success(f"VM '{vm_name}' undefined successfully.")
        return True
    except Exception as e:
        log.exception(f"An unexpected error occurred during VM undefine for '{vm_name}'", e)
        return False


def backup_vm_xml(vm_name: str, backup_dir: Union[str, Path], dry_run: bool = False) -> Optional[Path]: # Add dry_run
    """Backup VM XML file from libvirt."""
    log.info(f"Attempting to backup XML for VM '{vm_name}'... (Dry Run: {dry_run})")
    backup_path = Path(backup_dir)
    # Ensure backup dir exists even in dry run for path calculation
    if not ensure_directory_exists(backup_path, quiet=False):
        return None
    if not check_command_exists("virsh", quiet=True):
        log.warning("'virsh' command not found. Cannot backup VM XML.")
        return None
    try:
        # Keep quiet=True for initial check, log specific errors below
        success = True # Assume success for dry run initially
        xml_content = f"<!-- [Dry Run] XML content for {vm_name} -->" if dry_run else ""
        stderr = ""
        if not dry_run:
            success, xml_content, stderr = safe_run_virsh_command(["dumpxml", vm_name], quiet=True)
        else:
            log.info(f"[Dry Run] Would execute: virsh dumpxml {vm_name}")

        if not success:
            # Handle errors even in dry run simulation if needed, but actual command wasn't run
            stderr_lower = stderr.lower()
            if f"domain '{vm_name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                 log.error(f"VM '{vm_name}' not found, cannot backup XML.")
            elif "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 log.error(f"Permission error getting XML for VM '{vm_name}'. Check libvirt permissions.")
            else:
                 # Log other errors specifically
                 log.error(f"Failed to get XML for VM '{vm_name}': {stderr}")
            return None
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_file = backup_path / f"{vm_name}-{timestamp}.xml"
        if dry_run:
            log.info(f"[Dry Run] Would write XML backup to: {backup_file}")
            return backup_file # Return simulated path
        elif write_file_text(backup_file, xml_content, quiet=False):
            log.success(f"VM XML backed up to {backup_file}")
            return backup_file
        else:
            return None
    except Exception as e:
        log.exception(f"An unexpected error occurred during XML backup for '{vm_name}'", e)
        return None


def remove_vm(vm: VirtualMachine, keep_disks: bool = True,
              backup_dir: Optional[Path] = None,
              dry_run: bool = False) -> bool: # Add dry_run parameter
    """Remove a VM configuration (script/XML) and optionally undefine from libvirt.

    Args:
        vm: The VirtualMachine object to remove.
        keep_disks: If True, only undefine, don't remove storage (passed to undefine_vm).
        backup_dir: Optional directory to back up XML to.
        dry_run: If True, simulate actions without making changes.

    Returns:
        True if removal (or simulation) was successful, False otherwise.
    """
    log.info(f"Attempting to remove VM '{vm.name}' configuration and runtime... (Dry Run: {dry_run})")
    vm_removed_from_runtime = True # Assume success if not managed by runtime

    # 1. Undefine from Libvirt (if applicable and exists)
    if check_command_exists("virsh", quiet=True):
        # Check state via virsh first to see if it's defined
        state_success, _, state_stderr = safe_run_virsh_command(["domstate", vm.name], quiet=True)
        stderr_lower = state_stderr.lower() # Use lowercase for checks
        is_defined_in_virsh = False # Default to not defined
        permission_error_check = False # Flag for permission error

        if state_success:
            # If domstate command succeeds, the VM is definitely defined in libvirt
            is_defined_in_virsh = True
        else:
            # If domstate failed, check the reason
            if f"domain '{vm.name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                 log.debug(f"VM '{vm.name}' not found via virsh (domstate).")
                 is_defined_in_virsh = False
            elif "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 log.warning(f"Permission error checking state for VM '{vm.name}'. Cannot determine if defined in libvirt. Skipping libvirt removal steps.")
                 is_defined_in_virsh = False # Treat as not defined if we can't check due to permissions
                 permission_error_check = True # Flag that we hit a permission issue
            else:
                 # Log other errors but assume not defined for safety
                 log.warning(f"Could not determine libvirt definition status for VM '{vm.name}' due to unexpected error: {state_stderr}")
                 is_defined_in_virsh = False

        if is_defined_in_virsh:
            log.info(f"VM '{vm.name}' appears to be defined in libvirt. Attempting removal...")
            # Shutdown VM if running
            if "running" in vm.state: # Use the state determined earlier if available
                 # Pass dry_run status to shutdown_vm
                 if not shutdown_vm(vm.name, force=False, timeout=60, dry_run=dry_run):
                      # shutdown_vm handles logging, including dry run simulation
                      log.error(f"Failed to shutdown VM '{vm.name}' via libvirt (or simulation failed). Cannot safely remove.")
                      return False # Stop removal if shutdown fails

            # Backup XML if requested (pass dry_run status)
            if backup_dir:
                backup_vm_xml(vm.name, backup_dir, dry_run=dry_run) # Handles logging & dry run


            # Undefine VM (pass dry_run status)
            vm_removed_from_runtime = undefine_vm(vm.name, remove_storage=(not keep_disks), dry_run=dry_run) # Handles logging & dry run
            if not vm_removed_from_runtime:
                 # undefine_vm handles logging, including dry run simulation failure if applicable
                 log.error(f"Failed to undefine VM '{vm.name}' from libvirt (or simulation failed). Aborting script removal.")
                 # Decide if we should still remove script files? For safety, maybe not.
                 return False
        else:
            # Log why we are skipping (unless it was a permission error, already logged)
            if not permission_error_check:
                 log.info(f"VM '{vm.name}' not found in libvirt or definition status unknown, skipping libvirt undefine.")
            # If permission_error_check is True, the warning was already logged.
    else:
        log.info("virsh not found, skipping libvirt undefine step.")

    # 2. Remove Script File (if it exists)
    script_removed = True
    if vm.script_path and is_valid_file(vm.script_path, quiet=True):
        if dry_run:
            log.info(f"[Dry Run] Would remove VM script file: {vm.script_path}")
            script_removed = True # Simulate success
        else:
            log.info(f"Removing VM script file: {vm.script_path}")
            script_removed = delete_file(vm.script_path, quiet=False) # Use safe delete
        # Log success/failure based on actual or simulated result
        if script_removed:
             log.success(f"{'[Dry Run] Would have r' if dry_run else 'R'}emoved script file: {vm.script_path.name}")
        else:
             log.error(f"Failed to remove script file: {vm.script_path.name}")
             # Continue even if script removal fails? Maybe.

    # 3. Remove XML File (if it exists)
    xml_removed = True
    if vm.xml_path and is_valid_file(vm.xml_path, quiet=True):
        if dry_run:
            log.info(f"[Dry Run] Would remove VM XML file: {vm.xml_path}")
            xml_removed = True # Simulate success
        else:
            log.info(f"Removing VM XML file: {vm.xml_path}")
            xml_removed = delete_file(vm.xml_path, quiet=False) # Use safe delete
        # Log success/failure based on actual or simulated result
        if xml_removed:
             log.success(f"{'[Dry Run] Would have r' if dry_run else 'R'}emoved XML file: {vm.xml_path.name}")
        else:
             log.error(f"Failed to remove XML file: {vm.xml_path.name}")

    # 4. Delete disk images if keep_disks is False
    if not keep_disks and vm.disk_paths:
        from .disk_utils import DiskImage, delete_disk_image
        log.info(f"Removing disk images for VM '{vm.name}'... (Dry Run: {dry_run})")
        for disk_path in vm.disk_paths:
            # Skip if the path doesn't exist or isn't a file
            if not is_valid_file(disk_path, quiet=True):
                log.warning(f"Disk file not found or inaccessible: {disk_path}")
                continue
                
            # Create DiskImage object assuming it's not physical
            disk = DiskImage(disk_path, is_physical=False)
            
            # Delete using disk_utils for extra safety measures
            if dry_run:
                log.info(f"[Dry Run] Would delete disk file: {disk_path}")
            else:
                log.info(f"Deleting disk file: {disk_path}")
                if delete_disk_image(disk, quiet=False):  # Use disk_utils for safety
                    log.success(f"Deleted disk file: {disk_path.name}")
                else:
                    log.error(f"Failed to delete disk file: {disk_path.name}")

    # 5. Consider removing user blobs? This might be too destructive.
    #    Cleanup script should handle blob removal separately based on config.

    # Return overall success (primarily based on runtime removal if attempted)
    # If not managed by runtime, success depends on file removal.
    if not check_command_exists("virsh", quiet=True):
         return script_removed and xml_removed # Success if files removed
    else:
         return vm_removed_from_runtime # Success if undefine worked (or wasn't needed/skipped due to perms)
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
from .logger import default_logger as log, LogLevel

# Set log level to DEBUG to see all the VM name detection logs
# Fix: use min_level property instead of non-existent set_level method
log.min_level = LogLevel.DEBUG
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
        # Always display the VM's true name most prominently
        # If available, include script name as secondary info
        script_info = f" (Script: {self.script_path.name})" if self.script_path else ""
        # Show the VM name prominently - this is the name used for libvirt operations
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
    from .safe_command_utils import run_sudo_command
    
    state = "defined" # Default state if found via files but not running

    # 1. Check Libvirt state (always with sudo)
    if check_command_exists("virsh", quiet=True):
        # Always use sudo for virsh commands
        success, output, stderr = run_sudo_command(
            ["virsh", "domstate", vm_name],
            prompt="Libvirt operations require sudo to check VM state",
            quiet=True
        )
        
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
            elif stderr: # Log other errors
                 log.warning(f"Could not get libvirt state for VM '{vm_name}': {stderr}")
            # If not found, proceed to check QEMU processes

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
    Find macOS VMs using a simplified approach that primarily relies on virsh commands
    to identify UMK (ULTMOS) VMs, with fallback to script-based detection.
    
    This implementation uses a more conservative approach with scoring to ensure we only
    detect legitimate UMK VMs and avoid removing non-UMK VMs.
    """
    vms: Dict[str, VirtualMachine] = {}  # Use dict to deduplicate by name
    log.info("Searching for macOS VMs using simplified detection...")
    
    try:
        project_root = Path(__file__).resolve().parents[3]  # Path to project root
        
        # STEP 1: Check for boot.sh to get OS ID for improved matching
        boot_script_path = project_root / "boot.sh"
        os_id = ""
        id_val = "macOS"  # Default ID to use if not found
        boot_script_content = ""
        
        if is_valid_file(boot_script_path, quiet=True):
            try:
                boot_script_content = read_file_text(boot_script_path, quiet=True)
                os_id_match = re.search(r'OS_ID="([^"]+)"', boot_script_content)
                id_match = re.search(r'ID="([^"]+)"', boot_script_content)
                
                if os_id_match:
                    os_id = os_id_match.group(1)
                    log.debug(f"Found OS_ID in boot.sh: {os_id}")
                if id_match:
                    id_val = id_match.group(1)
                    log.debug(f"Found ID in boot.sh: {id_val}")
            except Exception as e:
                log.debug(f"Error reading boot.sh: {e}")
        
        # STEP 2: Use virsh to list all domains (ALWAYS with sudo)
        from .safe_command_utils import run_sudo_command
        
        log.info("Using virsh (with sudo) to detect macOS VMs...")
        
        # Always use sudo for virsh commands - this is required on many systems
        success, output, stderr = run_sudo_command(
            ["virsh", "list", "--all"],
            prompt="Libvirt operations require sudo to list VMs",
            quiet=True
        )
        
        if success:
            lines = output.strip().split('\n')
            if len(lines) > 2:  # Skip header lines
                # Process each domain line
                for line in lines[2:]:  # Skip header rows
                    # Example line: " 1  ultmos-12        shut off"
                    # Example line: " -  my-other-vm      running "
                    # Use regex for more robust parsing, specifically handling "shut off"
                    # Regex breakdown:
                    # \s*(\S+)       # Capture ID (non-whitespace) after optional leading space
                    # \s+           # Separator space
                    # (.*?)         # Capture Domain Name (non-greedy)
                    # \s+           # Separator space
                    # (running|shut off|paused|idle|pmsuspended|crashed|dying|unknown) # Capture known states
                    # \s*$          # Optional trailing space to end of line
                    match = re.match(r'\s*(\S+)\s+(.*?)\s+(running|shut off|paused|idle|pmsuspended|crashed|dying|unknown)\s*$', line, re.IGNORECASE)
                    if match:
                        _id, domain_name, domain_state = match.groups()
                        # Clean up trailing whitespace potentially captured in domain_name
                        domain_name = domain_name.rstrip()
                        log.debug(f"Parsed virsh line: ID='{_id}', Name='{domain_name}', State='{domain_state}'")
                    else:
                        log.warning(f"Could not parse virsh list line with known states: {line}")
                        # Fallback regex for potentially unknown states
                        fallback_match = re.match(r'\s*(\S+)\s+(.*?)\s+(\S+)\s*$', line)
                        if fallback_match:
                             _id, domain_name, domain_state = fallback_match.groups()
                             domain_name = domain_name.rstrip()
                             log.debug(f"Parsed virsh line (fallback): ID='{_id}', Name='{domain_name}', State='{domain_state}'")
                        else:
                            log.error(f"Failed to parse virsh list line completely: {line}")
                            continue # Skip malformed lines
                    
                    # Log that we are starting to process this specific VM
                    log.debug(f"Processing parsed VM: Name='{domain_name}', State='{domain_state}'")

                    # Implement a scoring system to identify UMK VMs
                    # Higher score = more likely to be a UMK VM
                    score = 0
                    reasons = [] # Corrected indentation

                    # Check for common UMK/macOS indicators in name
                    macos_indicators = [
                            "macOS", "Mac OS X", "ULTMOS",
                            "Monterey", "Ventura", "Sonoma", "Big Sur",
                            "Catalina", "Mojave", "High Sierra", "Sierra",
                            "El Capitan", "Yosemite", "Mavericks"
                        ]
                        
                    # Check boot.sh-derived names
                    boot_derived_names = []
                    if os_id:
                        boot_derived_names = [
                            f"{id_val} {os_id}",
                            f"macOS {os_id}",
                            f"Mac OS X {os_id}",
                            os_id
                        ]
                        
                        # Add highest score for exact match with boot.sh-derived name
                        if domain_name in boot_derived_names:
                            score += 10
                            reasons.append(f"Exact match with boot.sh OS_ID ({os_id})")
                    
                    # Check for macOS indicators in name (weighted)
                    for indicator in macos_indicators:
                            if indicator.lower() in domain_name.lower():
                                score += 5
                                reasons.append(f"Contains macOS indicator: {indicator}")
                                break
                    # Log the initial score based on name checks
                    log.debug(f"Initial score for {domain_name} based on name: {score} (Reasons: {reasons})")
                    # If we have at least some indication this might be a macOS VM, proceed with XML check
                    # Only proceed with XML check if initial score is > 0
                    if score > 0:
                        log.debug(f"Potential macOS VM found based on name: {domain_name} (Score: {score}, Reasons: {reasons})")

                        log.debug(f"Attempting to dump XML for {domain_name}...")
                        # Get XML to further verify and get disk paths (also with sudo)
                        xml_success, xml_content, xml_stderr = run_sudo_command(
                            ["virsh", "dumpxml", domain_name],
                            prompt="Libvirt operations require sudo to dump XML",
                            quiet=True
                        )
                        log.debug(f"XML dump for {domain_name} success: {xml_success}")

                        if xml_success:
                            # Check for UMK-specific indicators in XML
                            ultmos_indicators = [
                                "<type arch='x86_64' machine='q35'>hvm</type>",
                                "OVMF_CODE.fd",
                                "OVMF_VARS.fd",
                                "OpenCore.qcow2",
                                "macOS",
                                "Mac OS X",
                                "BaseSystem.img",
                                "HDD.qcow2",
                                "isa-applesmc",
                                "vmware-cpuid-freq=on",
                            ]

                            for indicator in ultmos_indicators:
                                if indicator in xml_content:
                                    score += 2
                                    reasons.append(f"XML contains UMK indicator: {indicator}")

                            # Additional check for boot directory structure in disk paths
                            if "boot/" in xml_content and ".qcow2" in xml_content:
                                score += 3
                                reasons.append("XML references boot/ directory with qcow2 files")
                            log.debug(f"Score after XML check for {domain_name}: {score}")
                            
                            # Only add VM if final score is high enough
                            if score >= 10: # Increased threshold back to 10
                                log.debug(f"Score threshold met for {domain_name}. Preparing to add VM.")
                                log.info(f"Confirmed macOS VM: {domain_name} (Score: {score})")
                                log.debug(f"Detection reasons: {', '.join(reasons)}")

                                # Extract disk paths
                                disk_paths = extract_disk_paths(xml_content)
                                log.debug(f"Extracted disk paths for {domain_name}: {[p.name for p in disk_paths]}")

                                # Try to find a matching boot script
                                script_path = None
                                if is_valid_file(boot_script_path, quiet=True):
                                    script_path = boot_script_path

                                # Get XML path
                                xml_path = extract_xml_path(domain_name)
                                log.debug(f"Extracted XML path for {domain_name}: {xml_path}")
                                
                                log.debug(f"Adding VM '{domain_name}' to dictionary...")
                                vms[domain_name] = VirtualMachine(
                                    name=domain_name,
                                    state=domain_state,
                                    script_path=script_path,
                                    xml_path=xml_path,
                                    disk_paths=disk_paths
                                )
                                log.info(f"Added VM to cleanup list: {vms[domain_name]}")
                                log.debug(f"Current VMs dictionary keys: {list(vms.keys())}")
                            else:
                                log.debug(f"Skipping VM {domain_name} - insufficient final confidence score ({score}) after XML check")
                        else:
                            log.warning(f"Failed to dump XML for potential VM {domain_name}: {xml_stderr}")
                            log.debug(f"Skipping {domain_name} due to XML dump failure.")
                    # else: # Implicitly skip if initial score is 0
                    #    log.debug(f"Skipping XML check for {domain_name} - initial score is 0") # Optional log
        else:
            # Couldn't list domains - permission issues?
            log.warning(f"Could not list libvirt domains with sudo: {stderr}")
            log.warning("If this is a permission issue, make sure your user can run sudo commands.")
        
        # STEP 3: Fall back to checking boot.sh if no VMs found via virsh
        if not vms and is_valid_file(boot_script_path, quiet=True):
            log.info("No VMs found via virsh. Falling back to boot.sh detection.")
            
            # Check if boot.sh exists and looks like a valid UMK script
            if "ULTMOS=" in boot_script_content or "OpenCore.qcow2" in boot_script_content:
                # Just create a VM entry for boot.sh
                vm_name = "boot"  # Default name
                
                # Try to extract a better name from boot.sh
                if os_id:
                    vm_name = f"{id_val} {os_id}"
                
                state = _get_vm_state(vm_name)  # This may not find anything
                
                # Look for disk files
                disk_paths_set: Set[Path] = set()
                
                # Check for common disk paths
                hdd_qcow2 = project_root / "HDD.qcow2"
                basesystem_img = project_root / "BaseSystem.img"
                basesystem_dmg = project_root / "BaseSystem.dmg"
                
                for path in [hdd_qcow2, basesystem_img, basesystem_dmg]:
                    if is_valid_file(path, quiet=True):
                        disk_paths_set.add(path)
                        log.debug(f"Added disk from boot.sh fallback: {path}")
                
                # Create VM entry
                vms[vm_name] = VirtualMachine(
                    name=vm_name,
                    state="unknown" if state == "defined" else state,
                    script_path=boot_script_path,
                    xml_path=None,
                    disk_paths=sorted(list(disk_paths_set))
                )
                
                log.info(f"Added VM via boot.sh fallback: {vms[vm_name]}")
        
    except Exception as e:
        log.exception("Unexpected error during VM discovery", e)
    
    if not vms:
        log.warning("No macOS VMs were found using the simplified detection method.")
    
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
            
            # Look for VM name in ALL possible blob files - this is crucial for matching with libvirt
            # List all potential blob files that might contain VM name, in priority order
            vm_name_blob_candidates = [
                blobs_user_dir / "USR_VM_NAME.apb",
                blobs_user_dir / "USR_TARGET_VM_NAME.apb",
                project_root / "blobs" / "USR_VM_NAME.apb",
                project_root / "blobs" / "USR_TARGET_VM_NAME.apb",
                blobs_user_dir / "USR_BOOT_NAME.apb",
                blobs_user_dir / "USR_DOMAIN_NAME.apb",
                project_root / "blobs" / "USR_BOOT_NAME.apb",
                project_root / "blobs" / "USR_DOMAIN_NAME.apb"
            ]
            
            log.debug(f"Checking for VM name in blob files for VM {vm_name}...")
            found_name = False
            
            try:
                # Try each candidate file
                for blob_path in vm_name_blob_candidates:
                    if is_valid_file(blob_path, quiet=True):
                        name_content = read_file_text(blob_path, quiet=True)
                        if name_content:
                            vm_name = name_content.strip()
                            log.debug(f"Found VM name in blob: {blob_path.name}: '{vm_name}' (was: {vm_name_orig})")
                            found_name = True
                            break
                
                # As a last resort, try to read from the script file itself to find VM name
                if not found_name and is_valid_file(script_path, quiet=True):
                    script_content = read_file_text(script_path, quiet=True)
                    if script_content:
                        # Look for common domain/VM name declarations in QEMU scripts
                        name_patterns = [
                            r'VM_NAME="([^"]+)"',
                            r'VM_NAME=\'([^\']+)\'',
                            r'VM_NAME=([^\s;]+)',
                            r'domain="([^"]+)"',
                            r'domain=\'([^\']+)\'',
                            r'domain=([^\s;]+)',
                            r'-name\s+([^,\s]+)',
                            r'-name\s+guest=([^,\s]+)'
                        ]
                        
                        import re
                        for pattern in name_patterns:
                            match = re.search(pattern, script_content)
                            if match:
                                vm_name = match.group(1).strip()
                                log.debug(f"Extracted VM name from script: '{vm_name}' (was: {vm_name_orig})")
                                found_name = True
                                break
            except Exception as e:
                log.warning(f"Error reading VM name for {vm_name_orig}: {e}")
                
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
    from .safe_command_utils import run_sudo_command

    # First try to get XML path directly from virsh (with sudo)
    try:
        success, output, _ = run_sudo_command(
            ["virsh", "domuuid", vm_name],
            prompt="Libvirt operations require sudo to get VM UUID",
            quiet=True
        )

        if success and output.strip():
            uuid = output.strip()

            # Common locations based on UUID
            uuid_locations = [
                Path("/etc/libvirt/qemu"),
                Path("/var/lib/libvirt/qemu")
            ]

            # Try to locate XML based on UUID (requires sudo)
            for base_location in uuid_locations:
                xml_path = base_location / f"{uuid}.xml"

                # Check if file exists and is readable using sudo head
                # This avoids using '&&' which might be flagged as unsafe
                file_check_cmd = ["head", "-n", "1", str(xml_path)]
                file_check_success, _, file_check_stderr = run_sudo_command(
                    file_check_cmd,
                    prompt="Checking XML file existence requires sudo",
                    quiet=True
                )

                # If head command succeeded (exit code 0), the file exists and is readable
                if file_check_success:
                    log.debug(f"Found XML path with sudo: {xml_path}")
                    return xml_path
                else:
                    # Log why head might have failed (e.g., file not found, permission denied even for root)
                    log.debug(f"sudo head check failed for {xml_path}: {file_check_stderr}")
    except Exception as e:
        log.debug(f"Error looking up XML via virsh: {e}")

    # Fallback to checking common locations
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
                    log.debug(f"Found XML path in standard location: {xml_path}")
                    return xml_path
        except PermissionError:
            log.debug(f"Permission denied checking libvirt XML location: {location}")
        except Exception as e:
            log.debug(f"Error checking libvirt XML location {location}: {e}")

    log.debug(f"Could not find XML path for VM: {vm_name}")
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
        success_state, state_output, stderr_state = safe_run_virsh_command( # Use safe alias with sudo fallback
            ["domstate", vm_name], quiet=True, try_sudo=True
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
            success_action, _, stderr_action = safe_run_virsh_command(action_cmd, quiet=False, try_sudo=True)
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
                    ["domstate", vm_name], quiet=True, try_sudo=True
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
                    ["destroy", vm_name], quiet=False, try_sudo=True
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
            success, _, stderr = safe_run_virsh_command(command, quiet=False, try_sudo=True)
        else:
            log.info(f"[Dry Run] Would execute: virsh {' '.join(command)}")

        if success:
            log.success(f"VM '{vm_name}' undefined successfully.")
            return True
        else:
            # Command failed, but check if it's because the VM is already undefined
            stderr_lower = stderr.lower()
            log.error(f"Failed to undefine VM '{vm_name}'. Exit code was non-zero.")
            if stderr:
                 log.error(f"Virsh stderr: {stderr.strip()}")
            # Check for "domain not found" errors - these should be treated as success
            if f"domain '{vm_name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                log.info(f"VM '{vm_name}' was already undefined.")
                return True # Treat as success when VM is already undefined
            return False # Other types of failures
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
            success, xml_content, stderr = safe_run_virsh_command(["dumpxml", vm_name], quiet=True, try_sudo=True)
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


def direct_remove_vm_with_sudo(vm_name: str, dry_run: bool = False) -> bool:
    """A simplified, direct approach to remove a VM using sudo commands directly.
    
    This function bypasses the complex detection and undefine logic and directly
    executes sudo commands to forcefully remove the VM.
    
    Args:
        vm_name: The name of the VM to remove
        dry_run: If True, simulate actions without making changes

    Returns:
        True if the operation was successful or simulated, False otherwise
    """
    log.info(f"Attempting direct VM removal with sudo for '{vm_name}'... (Dry Run: {dry_run})")
    
    try:
        # Skip all checks and directly run the forceful undefine command
        if dry_run:
            log.info(f"[Dry Run] Would execute: sudo virsh undefine --domain {vm_name} --remove-all-storage --nvram")
            return True
        else:
            import subprocess
            
            # Execute the command with all options for maximum chance of success
            log.info(f"Executing direct sudo virsh undefine for '{vm_name}'...")
            result = subprocess.run(
                ["sudo", "virsh", "undefine", "--domain", vm_name, "--remove-all-storage", "--nvram"],
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on error
            )
            
            # Check if command succeeded or if it failed because domain wasn't found (both count as success)
            if result.returncode == 0:
                log.success(f"Successfully removed VM '{vm_name}' with direct sudo command.")
                return True
            elif "failed to get domain" in result.stderr or "domain not found" in result.stderr:
                log.info(f"VM '{vm_name}' was already undefined (not found in virsh).")
                return True
            else:
                log.error(f"Failed to remove VM '{vm_name}' with direct sudo command: {result.stderr}")
                
                # One more attempt with the most basic command form
                log.warning(f"Attempting simplified fallback command for '{vm_name}'...")
                fallback = subprocess.run(
                    ["sudo", "virsh", "undefine", vm_name],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if fallback.returncode == 0:
                    log.success(f"Successfully removed VM '{vm_name}' with fallback command.")
                    return True
                else:
                    log.error(f"All attempts to remove VM '{vm_name}' failed. Last error: {fallback.stderr}")
                    return False
    except Exception as e:
        log.exception(f"Unexpected error during direct VM removal for '{vm_name}'", e)
        return False

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
        from .safe_command_utils import run_sudo_command # Import necessary functions
        
        # First try with dumpxml instead of domstate to verify if VM really exists
        # This is more reliable as it actually tries to access the domain XML
        # ALWAYS use sudo for the dumpxml check to avoid permission issues
        log.debug(f"Verifying VM '{vm.name}' existence using sudo virsh dumpxml...")
        dump_success, dump_output, dump_stderr = run_sudo_command(
            ["virsh", "dumpxml", vm.name],
            prompt="Libvirt operations require sudo to dump XML",
            quiet=True
        )
        
        stderr_lower = dump_stderr.lower() if dump_stderr else "" # Use lowercase for checks
        is_defined_in_virsh = False # Default to not defined
        permission_error_check = False # Flag for permission error

        if dump_success:
            # If dumpxml command succeeds, the VM is definitely defined in libvirt
            is_defined_in_virsh = True
            log.debug(f"VM '{vm.name}' exists in virsh (confirmed with sudo dumpxml).")
        else:
            # If dumpxml failed, check the reason
            if f"domain '{vm.name.lower()}' not found" in stderr_lower or "failed to get domain" in stderr_lower:
                 log.debug(f"VM '{vm.name}' not found via virsh (sudo dumpxml).")
                 is_defined_in_virsh = False
            elif "permission denied" in stderr_lower or "failed to connect" in stderr_lower or "authentication required" in stderr_lower:
                 # This shouldn't happen with sudo, but just in case
                 log.warning(f"Permission error checking for VM '{vm.name}' despite using sudo. This is unexpected.")
                 # Still attempt removal as there might be a libvirt connection issue rather than a permissions issue
                 is_defined_in_virsh = True
                 permission_error_check = True # Flag that we hit a permission issue
            else:
                 # For other errors, assume VM exists and try to remove it anyway
                 log.warning(f"Could not determine libvirt definition status for VM '{vm.name}' due to unexpected error: {dump_stderr}")
                 is_defined_in_virsh = True # Assume it exists and try to remove it

        # Get the VM name for consistent logging
        current_vm_name = vm.name
        
        # Always try our direct sudo approach first - this is the most reliable method
        if is_defined_in_virsh:
            log.info(f"VM '{current_vm_name}' detected in libvirt. Using direct sudo removal approach...")
            
            # Backup XML first if requested
            if backup_dir:
                log.debug(f"Backing up XML before removal for '{current_vm_name}'...")
                backup_vm_xml(current_vm_name, backup_dir, dry_run=dry_run)
            
            # Use the direct subprocess approach which has proven most reliable
            vm_removed_from_runtime = direct_remove_vm_with_sudo(current_vm_name, dry_run=dry_run)
            
            # If the direct approach failed, we'll continue with file cleanup anyway
            if not vm_removed_from_runtime:
                log.warning(f"Direct VM removal failed for '{current_vm_name}'. Will continue with file cleanup.")
        else:
            # Log why we are skipping (unless it was a permission error, already logged)
            if not permission_error_check:
                 log.info(f"VM '{vm.name}' not found in libvirt or definition status unknown, skipping libvirt undefine.")
            # If permission_error_check is True, the warning was already logged.
    else:
        log.info("virsh not found, skipping libvirt undefine step.")

    # 2. Remove Associated Files (Script and boot.xml)
    script_removed = True
    boot_xml_removed = True
    project_root = vm.script_path.parent if vm.script_path else None # Get project root if script path exists

    # Remove Script File (e.g., boot.sh)
    if vm.script_path and is_valid_file(vm.script_path, quiet=True):
        if dry_run:
            log.info(f"[Dry Run] Would remove VM script file: {vm.script_path}")
            script_removed = True # Simulate success
        else:
            log.info(f"Removing VM script file: {vm.script_path}")
            script_removed = delete_file(vm.script_path, quiet=False) # Use safe delete
        if script_removed:
             log.success(f"{'[Dry Run] Would have r' if dry_run else 'R'}emoved script file: {vm.script_path.name}")
        else:
             log.error(f"Failed to remove script file: {vm.script_path.name}")

    # Remove boot.xml if it exists in the project root
    if project_root:
        boot_xml_path = project_root / "boot.xml"
        if is_valid_file(boot_xml_path, quiet=True):
            if dry_run:
                log.info(f"[Dry Run] Would remove boot XML file: {boot_xml_path}")
                boot_xml_removed = True # Simulate success
            else:
                log.info(f"Removing boot XML file: {boot_xml_path}")
                boot_xml_removed = delete_file(boot_xml_path, quiet=False) # Use safe delete
            if boot_xml_removed:
                 log.success(f"{'[Dry Run] Would have r' if dry_run else 'R'}emoved boot XML file: {boot_xml_path.name}")
            else:
                 log.error(f"Failed to remove boot XML file: {boot_xml_path.name}")
        else:
            log.debug(f"boot.xml not found at {boot_xml_path}, skipping removal.")
            boot_xml_removed = True # Treat as success if not found

    # 3. Libvirt XML File - Handled by undefine.
    #    The virsh undefine command (called via undefine_vm in Step 1)
    #    should handle the removal of the libvirt-managed XML definition file.
    #    Attempting to delete vm.xml_path separately is redundant and could
    #    cause issues if it points to the system file. We only remove the script file.
    xml_removed = True # Assume success as undefine handles it

    # 4. Delete disk images if keep_disks is False
    if not keep_disks and vm.disk_paths:
        from .disk_utils import DiskImage, delete_disk_image
        log.info(f"Removing disk images for VM '{vm.name}'... (Dry Run: {dry_run})")
        for disk_path in vm.disk_paths:
            # --- Add check to skip OpenCore.qcow2 ---
            if disk_path.name == "OpenCore.qcow2":
                log.info(f"Preserving critical file: {disk_path.name}")
                continue
            # --- End check ---

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
         # Success depends on script and boot.xml removal if not managed by runtime
         return script_removed and boot_xml_removed
    else:
         # Success depends on runtime removal AND file removals
         return vm_removed_from_runtime and script_removed and boot_xml_removed
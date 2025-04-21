#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by kunihir0
https://github.com/kunihir0
https://github.com/Coopydood/ultimate-macOS-KVM
"""

import os
import time
import subprocess
import json
import sys
import argparse
import shutil
import tempfile
from datetime import datetime

# Import our temp file removal utility
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
try:
    from utils.remove_temp import clean_logs, clean_main_directory, clean_blobs_directory, clean_resources
except ImportError:
    print("Warning: Could not import remove_temp.py utility")

# Add the correct path to find the cpydColours module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'python')))

# Define fallback color class in case import fails
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    GRAY = '\u001b[38;5;245m'

# Try to import cpydColours but use our fallback if it fails
try:
    from cpydColours import color
except ImportError:
    # Already using the fallback color class defined above
    pass

# Check if we're in the correct directory
if not os.path.exists("./main.py"):
    print("Error: This script must be run from the root of the Ultimate macOS KVM directory.")
    sys.exit(1)

script = "cleanup.py"
scriptName = "Ultimate macOS KVM Uninstaller"
scriptID = "UNINST"
scriptVendor = "kunihir0"

# Parse command line arguments
parser = argparse.ArgumentParser("Uninstaller for Ultimate macOS KVM")
parser.add_argument("--downloads", dest="downloads", help="Clean downloaded recovery images", action="store_true")
parser.add_argument("--force", dest="force", help="Force uninstallation without confirmation", action="store_true")
parser.add_argument("--keep-data", dest="keepdata", help="Keep user data during uninstallation", action="store_true")
parser.add_argument("--vm-only", dest="vmonly", help="Remove only VM and VM data, keep repository", action="store_true")
parser.add_argument("--temp-files", dest="tempfiles", help="Clean temporary files created during VM setup", action="store_true")
args = parser.parse_args()

# Try to get version
try:
    with open("./.version", "r") as f:
        version = f.read().strip()
except:
    version = "Unknown"

def clear(): 
    print("\n" * 150)

def clean_downloaded_images(force=False):
    """Clean downloaded macOS recovery images"""
    print(f"\n{color.BOLD}{color.BLUE}Cleaning downloaded recovery images...{color.END}")
    
    download_files = [
        "./BaseSystem.dmg",
        "./BaseSystem.img",
        "./resources/BaseSystem.dmg",
        "./resources/BaseSystem.img",
        "./Install*.app",
        "./macOS*.dmg",
        "./OSX*.dmg",
        "./Install*.dmg"
    ]
    
    # Count downloads
    download_count = 0
    for file_pattern in download_files:
        if "*" in file_pattern:
            import glob
            matching_files = glob.glob(file_pattern)
            download_count += len(matching_files)
        elif os.path.exists(file_pattern):
            download_count += 1
    
    if download_count == 0:
        print(f"  {color.YELLOW}No downloaded recovery images found to clean.{color.END}")
        return 0
    
    # Confirmation
    if not force:
        print(f"  Found {download_count} downloaded macOS recovery images to clean.")
        confirmation = input(f"  {color.BOLD}Continue with cleaning downloaded recovery images? (y/n): {color.END}")
        if confirmation.lower() not in ['y', 'yes']:
            print(f"  {color.YELLOW}Skipped cleaning downloaded recovery images.{color.END}")
            return 0
    
    # Clean downloads
    cleaned_count = 0
    for file_pattern in download_files:
        if "*" in file_pattern:
            import glob
            matching_files = glob.glob(file_pattern)
            for file_path in matching_files:
                try:
                    os.remove(file_path)
                    print(f"  {color.GREEN}✓{color.END} Removed: {file_path}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"  {color.RED}✗{color.END} Failed to remove {file_path}: {str(e)}")
        elif os.path.exists(file_pattern):
            try:
                os.remove(file_pattern)
                print(f"  {color.GREEN}✓{color.END} Removed: {file_pattern}")
                cleaned_count += 1
            except Exception as e:
                print(f"  {color.RED}✗{color.END} Failed to remove {file_pattern}: {str(e)}")
    
    print(f"  {color.GREEN}Cleaned {cleaned_count} downloaded recovery images.{color.END}")
    return cleaned_count

def clean_temporary_files(force=False):
    """Clean temporary files using the remove_temp.py utility"""
    print(f"\n{color.BOLD}{color.BLUE}Cleaning temporary files...{color.END}")
    
    # Check if we have the imported functions from remove_temp.py
    if 'clean_logs' not in globals() or 'clean_main_directory' not in globals() or 'clean_blobs_directory' not in globals() or 'clean_resources' not in globals():
        print(f"  {color.YELLOW}remove_temp.py utility not available. Skipping temporary file cleanup.{color.END}")
        return 0
    
    # Confirmation
    if not force:
        print(f"  This will remove all temporary files created during the VM setup process.")
        confirmation = input(f"  {color.BOLD}Continue with cleaning temporary files? (y/n): {color.END}")
        if confirmation.lower() not in ['y', 'yes']:
            print(f"  {color.YELLOW}Skipped cleaning temporary files.{color.END}")
            return 0
    
    # Use the imported functions from remove_temp.py
    total_removed = 0
    try:
        print(f"  {color.BLUE}Cleaning log files...{color.END}")
        total_removed += clean_logs()
        
        print(f"  {color.BLUE}Cleaning main directory...{color.END}")
        total_removed += clean_main_directory()
        
        print(f"  {color.BLUE}Cleaning blob files...{color.END}")
        total_removed += clean_blobs_directory()
        
        print(f"  {color.BLUE}Cleaning resource files...{color.END}")
        total_removed += clean_resources()
        
        print(f"  {color.GREEN}Successfully cleaned {total_removed} temporary files.{color.END}")
    except Exception as e:
        print(f"  {color.RED}Error during temp file cleanup: {str(e)}{color.END}")
        return 0
    
    return total_removed

def remove_vm_data_only(force=False):
        """Remove VM and VM data without uninstalling ULTMOS repository"""
        print(f"\n{color.BOLD}{color.BLUE}REMOVING VM AND VM DATA ONLY{color.END}")
        
        # Warning
        print(f"\n{color.BOLD}{color.YELLOW}WARNING: This will remove VMs and VM data only{color.END}")
        print(f"{color.YELLOW}This operation will:{color.END}")
        print(f"  - Remove VMs from virt-manager if found")
        print(f"  - Delete all VM disk images in the disks/ directory")
        print(f"  - Handle any disk images in the root directory")
        print(f"  - Keep the ULTMOS repository intact")
        
        # Check for VMs in virt-manager
        virt_vms = check_virtmanager_vms()
        
        # Check for running QEMU processes
        running_vms = check_running_vms()
        
        # Check for root directory disk images
        root_disk_images = check_root_disk_images()
        
        # Confirmation
        if not force:
            print(f"\n{color.BOLD}Type {color.YELLOW}REMOVE-VM{color.END}{color.BOLD} to proceed or anything else to cancel: {color.END}")
            confirmation = input()
            if confirmation != "REMOVE-VM":
                print(f"\n{color.YELLOW}VM removal cancelled.{color.END}")
                return 0
        
        # Remove VMs from virt-manager if found
        if virt_vms:
            if not force:
                print(f"\n{color.YELLOW}Do you want to remove the ULTMOS VMs from virt-manager? (y/n): {color.END}")
                vm_confirmation = input()
                if vm_confirmation.lower() in ['y', 'yes']:
                    remove_virtmanager_vms(virt_vms)
                else:
                    print(f"  {color.YELLOW}VMs will be kept in virt-manager.{color.END}")
            else:
                # Force removal of VMs
                remove_virtmanager_vms(virt_vms)
        
        # Stop running QEMU processes
        if running_vms:
            stop_running_vms(running_vms, force)
        
        # Handle root disk images
        if root_disk_images:
            handle_root_disk_images(root_disk_images, force)
        
        # Check and unmount any mounted images
        check_mounted_images()
        
        # Remove disk directory
        disks_dir = os.path.join(os.path.abspath("."), "disks")
        if os.path.exists(disks_dir):
            try:
                print(f"\n{color.BOLD}Removing VM disk images...{color.END}")
                # List all files to be deleted
                files_found = False
                for root, dirs, files in os.walk(disks_dir):
                    for file in files:
                        files_found = True
                        file_path = os.path.join(root, file)
                        print(f"  Removing: {file_path}")
                
                if not files_found:
                    print(f"  {color.YELLOW}No files found in disks directory.{color.END}")
                    
                # Actually remove the directory
                shutil.rmtree(disks_dir)
                print(f"\n{color.GREEN}✓{color.END} Successfully removed all VM disk images.")
                
                # Create an empty disks directory to maintain project structure
                os.makedirs(disks_dir, exist_ok=True)
                print(f"  {color.GREEN}✓{color.END} Created empty disks directory.")
                
                return 1
            except Exception as e:
                print(f"\n{color.RED}Error removing VM disk images: {str(e)}{color.END}")
                return 0
        else:
            print(f"\n{color.YELLOW}No VM disk directory found.{color.END}")
            print(f"  {color.BLUE}Creating disks directory to maintain project structure...{color.END}")
            
            try:
                os.makedirs(disks_dir, exist_ok=True)
                print(f"  {color.GREEN}✓{color.END} Created empty disks directory.")
                return 1
            except Exception as e:
                print(f"  {color.RED}✗{color.END} Failed to create disks directory: {str(e)}")
                return 0

def check_mounted_images():
    """Check for mounted qcow2 images and try to unmount them"""
    print(f"\n{color.BOLD}{color.BLUE}Checking for mounted images...{color.END}")
    
    # Check for mounted NBD devices (commonly used for qcow2 mounting)
    try:
        result = subprocess.run(['sudo', 'lsof', '+c', '0', '/dev/nbd*'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "OpenCore.qcow2" in result.stdout or "BaseSystem.img" in result.stdout:
            print(f"  {color.YELLOW}Found mounted qcow2 images. Attempting to unmount...{color.END}")
            
            # Try to unmount using the nbdassistant script if it exists
            if os.path.exists("./scripts/hyperchromiac/nbdassistant.py"):
                subprocess.run(['sudo', './scripts/hyperchromiac/nbdassistant.py', '-u', '-q'], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  {color.GREEN}✓{color.END} Unmounted qcow2 images.")
            else:
                print(f"  {color.YELLOW}NBD unmount script not found. Some files may be locked.{color.END}")
                return False
            return True
    except Exception as e:
        print(f"  {color.YELLOW}Warning: Could not check for mounted images: {str(e)}{color.END}")
    
    return True

def check_root_disk_images():
    """Check for disk images in the root directory that might conflict with autopilot"""
    print(f"\n{color.BOLD}{color.BLUE}Checking for disk images in root directory...{color.END}")
    
    root_dir = os.path.abspath(".")
    root_images = []
    
    # Common disk image patterns
    disk_patterns = [
        "*.qcow2",
        "*.img",
        "*.raw",
        "*.vdi",
        "*.vmdk",
        "HDD*"
    ]
    
    # Find all disk images in root directory
    for pattern in disk_patterns:
        import glob
        matching_files = glob.glob(os.path.join(root_dir, pattern))
        # Filter out known system files like BaseSystem.img and OpenCore.qcow2 in boot/
        filtered_files = [f for f in matching_files if not (
            "boot/OpenCore.qcow2" in f or
            "BaseSystem.img" in f or
            "/resources/" in f or
            "/boot/" in f
        )]
        root_images.extend(filtered_files)
    
    # Report findings
    if root_images:
        print(f"  {color.YELLOW}Found {len(root_images)} disk images in root directory:{color.END}")
        for img in root_images:
            print(f"  - {os.path.basename(img)}")
    else:
        print(f"  {color.GREEN}No disk images found in root directory.{color.END}")
        
    return root_images

def handle_root_disk_images(disk_images, force=False):
    """Handle disk images found in the root directory"""
    if not disk_images:
        return True
    
    print(f"\n{color.BOLD}{color.YELLOW}Disk images found in root directory need attention{color.END}")
    print(f"  These disk images may conflict with autopilot if you reinstall.")
    
    # Present options
    if not force:
        print(f"\n  {color.BOLD}What would you like to do?{color.END}")
        print(f"  1. Move to 'disks/' directory (recommended)")
        print(f"  2. Delete disk images")
        print(f"  3. Keep as is (may cause conflicts with autopilot)")
        
        choice = input(f"\n  {color.BOLD}Choice [1-3]: {color.END}")
        
        if choice == "1":
            # Create disks directory if it doesn't exist
            disks_dir = os.path.join(os.path.abspath("."), "disks")
            os.makedirs(disks_dir, exist_ok=True)
            
            # Move each file
            for disk_path in disk_images:
                disk_name = os.path.basename(disk_path)
                target_path = os.path.join(disks_dir, disk_name)
                
                # Check if target already exists
                if os.path.exists(target_path):
                    print(f"  {color.YELLOW}Warning: {disk_name} already exists in disks/{color.END}")
                    overwrite = input(f"  Overwrite? (y/n): ")
                    if overwrite.lower() not in ['y', 'yes']:
                        print(f"  {color.YELLOW}Skipping {disk_name}{color.END}")
                        continue
                
                try:
                    print(f"  Moving {disk_name} to disks/ directory...")
                    shutil.move(disk_path, target_path)
                    print(f"  {color.GREEN}✓{color.END} Successfully moved {disk_name}")
                except Exception as e:
                    print(f"  {color.RED}✗{color.END} Failed to move {disk_name}: {str(e)}")
            
            return True
            
        elif choice == "2":
            # Delete confirmation
            print(f"\n  {color.RED}WARNING: This will permanently delete the disk images.{color.END}")
            confirm = input(f"  {color.BOLD}Type 'DELETE' to confirm: {color.END}")
            
            if confirm != "DELETE":
                print(f"  {color.YELLOW}Deletion cancelled.{color.END}")
                return False
                
            # Delete each file
            for disk_path in disk_images:
                try:
                    print(f"  Deleting {os.path.basename(disk_path)}...")
                    os.remove(disk_path)
                    print(f"  {color.GREEN}✓{color.END} Successfully deleted {os.path.basename(disk_path)}")
                except Exception as e:
                    print(f"  {color.RED}✗{color.END} Failed to delete {os.path.basename(disk_path)}: {str(e)}")
            
            return True
            
        elif choice == "3":
            print(f"\n  {color.YELLOW}Keeping disk images in root directory.{color.END}")
            print(f"  {color.YELLOW}Note: This may cause conflicts if you run autopilot again.{color.END}")
            return True
            
        else:
            print(f"\n  {color.RED}Invalid choice. Keeping disk images as is.{color.END}")
            return False
    else:
        # In force mode, move to disks/
        disks_dir = os.path.join(os.path.abspath("."), "disks")
        os.makedirs(disks_dir, exist_ok=True)
        
        for disk_path in disk_images:
            try:
                disk_name = os.path.basename(disk_path)
                target_path = os.path.join(disks_dir, disk_name)
                print(f"  Moving {disk_name} to disks/ directory...")
                
                # Handle existing files in force mode by overwriting
                if os.path.exists(target_path):
                    os.remove(target_path)
                
                shutil.move(disk_path, target_path)
                print(f"  {color.GREEN}✓{color.END} Successfully moved {disk_name}")
            except Exception as e:
                print(f"  {color.RED}✗{color.END} Failed to handle {os.path.basename(disk_path)}: {str(e)}")
        
        return True

def check_virtmanager_vms():
    """Check for Ultimate macOS KVM VMs imported into virt-manager"""
    print(f"\n{color.BOLD}{color.BLUE}Checking for VMs in virt-manager...{color.END}")
    
    # Check if virsh is available
    try:
        result = subprocess.run(['which', 'virsh'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"  {color.YELLOW}virt-manager/virsh not found. Skipping VM check.{color.END}")
            return []
    except Exception:
        print(f"  {color.YELLOW}Could not check for virsh. Skipping VM check.{color.END}")
        return []
    
    # Try both user-level and system-level approaches
    ultmos_vms = []
    
    # Try user-level first (no sudo)
    try:
        print(f"  {color.BLUE}Checking for VMs at user level...{color.END}")
        result = subprocess.run(['virsh', 'list', '--all', '--name'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            vm_list = result.stdout.strip().split('\n')
            ultmos_vms = process_vm_list(vm_list, False)  # False = no sudo
    except Exception as e:
        print(f"  {color.YELLOW}Error checking for user-level VMs: {str(e)}{color.END}")
    
    # If no VMs found at user level, try system level with sudo
    if not ultmos_vms:
        try:
            print(f"  {color.BLUE}Checking for VMs at system level (sudo)...{color.END}")
            result = subprocess.run(['sudo', 'virsh', 'list', '--all', '--name'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                vm_list = result.stdout.strip().split('\n')
                ultmos_vms = process_vm_list(vm_list, True)  # True = use sudo
        except Exception as e:
            print(f"  {color.YELLOW}Error checking for system-level VMs: {str(e)}{color.END}")
    
    # Report findings
    if ultmos_vms:
        print(f"  {color.YELLOW}Found {len(ultmos_vms)} ULTMOS VM(s) in virt-manager:{color.END}")
        for vm in ultmos_vms:
            print(f"  - {vm}")
    else:
        print(f"  {color.GREEN}No ULTMOS VMs found in virt-manager.{color.END}")
    
    return ultmos_vms

def process_vm_list(vm_list, use_sudo):
    """Process a list of VMs and filter for ULTMOS VMs"""
    ultmos_vms = []
    
    for vm in vm_list:
        vm = vm.strip()
        if not vm:  # Skip empty lines
            continue
            
        # Check if this is an Ultimate macOS KVM VM by examining its XML definition
        try:
            if use_sudo:
                xml_result = subprocess.run(['sudo', 'virsh', 'dumpxml', vm],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                xml_result = subprocess.run(['virsh', 'dumpxml', vm],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
            if xml_result.returncode != 0:
                continue  # Skip if we can't get XML
                
            xml_content = xml_result.stdout
            
            # Look specifically for Ultimate macOS KVM identifiers in the XML
            is_ultmos_vm = False
            
            # Check for specific identifiers in the VM XML
            if "ULTMOS" in xml_content:
                is_ultmos_vm = True
            if "ultimate-macOS-KVM" in xml_content or "Ultimate macOS KVM" in xml_content:
                is_ultmos_vm = True
            if "OpenCore.qcow2" in xml_content and ("macOS" in vm or "OSX" in vm):
                is_ultmos_vm = True
            
            if is_ultmos_vm:
                ultmos_vms.append(vm)
        except Exception:
            # Skip this VM if we can't get its XML
            continue
    
    return ultmos_vms

def remove_virtmanager_vms(vm_list):
    """Remove ULTMOS VMs from virt-manager"""
    if not vm_list:
        return True
        
    print(f"\n{color.BOLD}{color.YELLOW}Removing ULTMOS VMs from virt-manager...{color.END}")
    
    success = True
    for vm in vm_list:
        print(f"  Attempting to remove VM: {vm}")
        
        # Try both user and system level removal (first without sudo, then with sudo)
        sudo_levels = [False, True]  # First False (no sudo), then True (with sudo)
        vm_removed = False
        
        for use_sudo in sudo_levels:
            if vm_removed:
                break
                
            try:
                # Command prefix based on sudo level
                cmd_prefix = ['sudo'] if use_sudo else []
                sudo_text = "with sudo" if use_sudo else "without sudo"
                print(f"  Trying {sudo_text}...")
                
                # Try to destroy the VM first (if running)
                destroy_cmd = cmd_prefix + ['virsh', 'destroy', vm]
                subprocess.run(destroy_cmd,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                           
                # Try to undefine VM with NVRAM and storage removal
                undefine_cmd = cmd_prefix + ['virsh', 'undefine', vm, '--remove-all-storage', '--nvram']
                result = subprocess.run(undefine_cmd,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0:
                    print(f"  {color.GREEN}✓{color.END} Removed VM: {vm} {sudo_text}")
                    vm_removed = True
                    break
                    
                # Try again without storage removal
                undefine_cmd = cmd_prefix + ['virsh', 'undefine', vm, '--nvram']
                result = subprocess.run(undefine_cmd,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                   
                if result.returncode == 0:
                    print(f"  {color.GREEN}✓{color.END} Removed VM (storage may remain): {vm} {sudo_text}")
                    vm_removed = True
                    break
                
                # Try one last time without nvram flag
                undefine_cmd = cmd_prefix + ['virsh', 'undefine', vm]
                result = subprocess.run(undefine_cmd,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                   
                if result.returncode == 0:
                    print(f"  {color.GREEN}✓{color.END} Removed VM (nvram may remain): {vm} {sudo_text}")
                    vm_removed = True
                    break
                    
                # If we're on the last attempt (with sudo) and still failing, show error
                if use_sudo:
                    print(f"  {color.YELLOW}Failed with error: {result.stderr.strip()}{color.END}")
                
            except Exception as e:
                if use_sudo:  # Only show error on last attempt
                    print(f"  {color.RED}✗{color.END} Error removing VM {vm}: {str(e)}")
        
        # Check final removal status
        if not vm_removed:
            print(f"  {color.RED}✗{color.END} Failed to remove VM: {vm} after multiple attempts")
            success = False
            
    return success

def check_running_vms():
    """Check for running QEMU processes that might be Ultimate macOS KVM VMs"""
    print(f"\n{color.BOLD}{color.BLUE}Checking for running QEMU processes...{color.END}")
    
    try:
        # Look for QEMU processes running macOS VMs (common patterns in cmdline)
        result = subprocess.run(['ps', 'aux'], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            
        if result.returncode != 0:
            print(f"  {color.YELLOW}Unable to check for running processes.{color.END}")
            return []
            
        running_vms = []
        ultmos_indicators = ["OpenCore.qcow2", "-name macOS", "ULTMOS", 
                            f"{os.path.abspath('.')}/boot/OpenCore.qcow2",
                            f"{os.path.abspath('.')}/disks/"]
        
        for line in result.stdout.splitlines():
            line = line.lower()
            if "qemu" in line and any(indicator.lower() in line for indicator in ultmos_indicators):
                # Extract PID from the line
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        pid = parts[1]
                        running_vms.append(pid)
                        print(f"  {color.YELLOW}Found running QEMU process: PID {pid}{color.END}")
                    except (ValueError, IndexError):
                        pass
        
        if not running_vms:
            print(f"  {color.GREEN}No running macOS VMs found.{color.END}")
            
        return running_vms
    except Exception as e:
        print(f"  {color.YELLOW}Error checking for running processes: {str(e)}{color.END}")
        return []

def stop_running_vms(pids, force=False):
    """Try to gracefully stop running QEMU processes"""
    if not pids:
        return True
        
    print(f"\n{color.BOLD}{color.YELLOW}Found running macOS VMs that need to be stopped{color.END}")
    
    # Get confirmation unless forced
    if not force:
        print(f"  {color.YELLOW}Running VMs must be stopped to continue.{color.END}")
        confirmation = input(f"  {color.BOLD}Stop running VMs? (y/n): {color.END}")
        if confirmation.lower() not in ['y', 'yes']:
            print(f"  {color.YELLOW}Operation cancelled. Please shut down your VMs manually.{color.END}")
            return False
    
    success = True
    for pid in pids:
        try:
            print(f"  Trying to gracefully stop VM with PID {pid}...")
            # First try SIGTERM for graceful shutdown
            subprocess.run(['kill', pid], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a bit and check if process is gone
            time.sleep(2)
            if subprocess.run(['ps', '-p', pid], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                print(f"  {color.GREEN}✓{color.END} Successfully stopped VM with PID {pid}")
                continue
                
            # If still running, ask before using SIGKILL
            if not force:
                print(f"  {color.YELLOW}VM with PID {pid} is still running. Force kill? (y/n): {color.END}")
                force_kill = input()
                if force_kill.lower() not in ['y', 'yes']:
                    print(f"  {color.YELLOW}VM with PID {pid} was not stopped.{color.END}")
                    success = False
                    continue
            
            # Force kill with SIGKILL
            subprocess.run(['kill', '-9', pid], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(1)
            
            if subprocess.run(['ps', '-p', pid], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                print(f"  {color.GREEN}✓{color.END} Successfully force-killed VM with PID {pid}")
            else:
                print(f"  {color.RED}✗{color.END} Failed to stop VM with PID {pid}")
                success = False
        except Exception as e:
            print(f"  {color.RED}✗{color.END} Error stopping VM with PID {pid}: {str(e)}")
            success = False
    
    return success

def create_self_destruct_script(directory, keep_user_data=False, virt_vms=None):
    """Create a temporary script that will delete the Ultimate macOS KVM directory after this script terminates"""
    # Create a temp file for our self-destruct script
    fd, path = tempfile.mkstemp(suffix='.sh')
    try:
        user_data_dir = os.path.join(directory, "disks")
        # Define the backup directory regardless of whether we'll use it
        temp_backup_dir = os.path.expanduser("~/ultmos_user_data_backup")
        
        script_content = f"""#!/bin/bash
# Wait for the parent process to exit
sleep 2

echo "Removing Ultimate macOS KVM directory: {directory}"
"""
        
        # Add virsh VM removal if needed
        if virt_vms:
            script_content += f"""
# Removing related VMs from virt-manager
echo "Removing ULTMOS VMs from virt-manager..."
"""
            for vm in virt_vms:
                script_content += f"""
# Try both with and without sudo
virsh destroy "{vm}" 2>/dev/null || sudo virsh destroy "{vm}" 2>/dev/null
virsh undefine "{vm}" --remove-all-storage --nvram 2>/dev/null || sudo virsh undefine "{vm}" --remove-all-storage --nvram 2>/dev/null || virsh undefine "{vm}" --nvram 2>/dev/null || sudo virsh undefine "{vm}" --nvram 2>/dev/null || virsh undefine "{vm}" 2>/dev/null || sudo virsh undefine "{vm}" 2>/dev/null
"""
        
        # If we're keeping user data, move it to a temp location first
        if keep_user_data and os.path.exists(user_data_dir):
            script_content += f"""
# Create backup directory
mkdir -p "{temp_backup_dir}"

# Copy user data before deletion
if [ -d "{user_data_dir}" ]; then
  echo "Backing up user data to {temp_backup_dir}"
  cp -r "{user_data_dir}" "{temp_backup_dir}/"
fi
"""

        script_content += f"""
# Remove everything
rm -rf "{directory}"

echo "Ultimate macOS KVM has been completely removed."

if [ -d "{temp_backup_dir}" ]; then
  echo "Your virtual disk images have been backed up to: {temp_backup_dir}"
fi
"""
        
        # Write the script
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(script_content)
        
        # Make it executable
        os.chmod(path, 0o755)
        return path
    except Exception as e:
        print(f"  {color.RED}Failed to create self-destruct script: {str(e)}{color.END}")
        try:
            os.unlink(path)
        except:
            pass
        return None

def uninstall_ultimate_macos_kvm(force=False, keep_data=False):
    """Complete self-destructing uninstallation of Ultimate macOS KVM"""
    print(f"\n{color.BOLD}{color.RED}UNINSTALLING ULTMOS...{color.END}")
    
    # Serious warning
    print(f"\n{color.BOLD}{color.RED}WARNING: THIS WILL COMPLETELY REMOVE Ultimate macOS KVM!{color.END}")
    print(f"{color.YELLOW}This is a permanent operation that will:{color.END}")
    print(f"  - Delete ALL ULTMOS files, scripts, and configurations")
    print(f"  - Remove all downloaded macOS images")
    
    if keep_data:
        print(f"\n{color.GREEN}User data (virtual disks) will be backed up to your home directory.{color.END}")
    else:
        print(f"  - {color.RED}DELETE ALL YOUR VIRTUAL DISK IMAGES{color.END}")
    
    # Check for VMs in virt-manager
    virt_vms = check_virtmanager_vms()
    if virt_vms:
        print(f"\n{color.RED}WARNING: Found ULTMOS VMs in virt-manager!{color.END}")
        print(f"These will also be removed during uninstallation.")
    
    # Check for running QEMU processes
    running_vms = check_running_vms()
    if running_vms:
        print(f"\n{color.RED}WARNING: Found running macOS VMs started directly!{color.END}")
        print(f"These will also be stopped during uninstallation.")
    
    # Check for disk images in the root directory
    root_disk_images = check_root_disk_images()
    if root_disk_images:
        handle_root_disk_images(root_disk_images, force)
    
    # Confirmation - require typing "UNINSTALL" to proceed
    if not force:
        print(f"\n{color.BOLD}This action cannot be undone. Type {color.RED}UNINSTALL{color.END}{color.BOLD} to proceed or anything else to cancel: {color.END}")
        confirmation = input()
        if confirmation != "UNINSTALL":
            print(f"\n{color.YELLOW}Uninstallation cancelled.{color.END}")
            return 0
        
        # If VMs were found, ask for specific confirmation
        if virt_vms and not force:
            print(f"\n{color.YELLOW}Do you want to remove the ULTMOS VMs from virt-manager? (y/n): {color.END}")
            vm_confirmation = input()
            if vm_confirmation.lower() not in ['y', 'yes']:
                print(f"  {color.YELLOW}VMs will be kept in virt-manager.{color.END}")
                virt_vms = []
        
        # If running VMs were found, ask for specific confirmation
        if running_vms and not force:
            print(f"\n{color.YELLOW}Do you want to stop the running macOS VMs? (y/n): {color.END}")
            running_confirmation = input()
            if running_confirmation.lower() not in ['y', 'yes']:
                print(f"  {color.YELLOW}Running VMs will not be stopped.{color.END}")
                running_vms = []
    
    # Check and unmount any mounted images
    if not check_mounted_images():
        print(f"\n{color.YELLOW}Warning: Some files may be in use and cannot be deleted.{color.END}")
        if not force:
            print(f"Use --force to attempt deletion anyway.")
            return 0
    
    # Stop running QEMU processes
    if running_vms:
        stop_running_vms(running_vms, force)
    
    # Determine the Ultimate macOS KVM root directory (absolute path)
    ultmos_root = os.path.abspath(".")
    
    # Create the self-destruct script
    self_destruct_script = create_self_destruct_script(ultmos_root, keep_data, virt_vms)
    if not self_destruct_script:
        print(f"\n{color.RED}Failed to prepare uninstallation. Cannot continue.{color.END}")
        return 0
    
    print(f"\n{color.GREEN}Uninstallation prepared. Ultimate macOS KVM will now be completely removed.{color.END}")
    print(f"The uninstallation will proceed as soon as you press Enter.")
    input(f"{color.BOLD}Press Enter to begin uninstallation...{color.END}")
    
    # Execute the self-destruct script
    try:
        subprocess.Popen(['sudo', self_destruct_script], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         start_new_session=True)
        print(f"\n{color.GREEN}Uninstallation in progress...{color.END}")
        print(f"You can close this terminal now. Ultimate macOS KVM is being removed.")
        # Exit immediately to allow the self-destruct script to do its work
        sys.exit(0)
    except Exception as e:
        print(f"\n{color.RED}Failed to start uninstallation: {str(e)}{color.END}")
        # Try to delete the script
        try:
            os.unlink(self_destruct_script)
        except:
            pass
        return 0

def show_menu():
    """Show the main cleanup menu"""
    clear()
    print(f"\n\n   {color.BOLD}{color.RED}ULTMOS UNINSTALLER{color.END}")
    print(f"   by {color.BOLD}{scriptVendor}{color.END}\n")
    print(f"   This tool allows you to clean up or completely remove Ultimate macOS KVM.\n")
    
    # Check if there are any VM resources to clean up
    has_vms = False
    vms_found = check_virtmanager_vms()
    if vms_found:
        has_vms = True
    
    # Check if there are disk images to delete
    has_disk_images = False
    disks_dir = os.path.join(os.path.abspath("."), "disks")
    if os.path.exists(disks_dir):
        for root, dirs, files in os.walk(disks_dir):
            if files:
                has_disk_images = True
                break
    
    # Check if there are downloaded images
    has_downloads = False
    download_files = [
        "./BaseSystem.dmg",
        "./BaseSystem.img",
        "./resources/BaseSystem.dmg",
        "./resources/BaseSystem.img",
        "./Install*.app",
        "./macOS*.dmg",
        "./OSX*.dmg",
        "./Install*.dmg"
    ]
    
    for file_pattern in download_files:
        if "*" in file_pattern:
            import glob
            if glob.glob(file_pattern):
                has_downloads = True
                break
        elif os.path.exists(file_pattern):
            has_downloads = True
            break
    
    print(f"{color.BOLD}      1. Clean downloaded macOS images")
    if has_downloads:
        print(f"{color.END}         Removes downloaded recovery and installation files\n")
    else:
        print(f"{color.GRAY}         No downloaded images found{color.END}\n")
    
    print(f"{color.BOLD}      2. {color.YELLOW}Remove VM and VM data only{color.END}")
    if has_vms or has_disk_images:
        resources = []
        if has_vms:
            resources.append("VMs from virt-manager")
        if has_disk_images:
            resources.append("disk images")
        print(f"{color.END}         Removes {' and '.join(resources)}\n         while keeping the ULTMOS repository intact\n")
    else:
        print(f"{color.GRAY}         No VMs or disk images found to remove{color.END}\n")
    
    print(f"{color.BOLD}      3. {color.RED}Uninstall ULTMOS (keep virtual disks){color.END}")
    print(f"{color.END}         Completely removes Ultimate macOS KVM but backs up your VM disk images\n")
    
    print(f"{color.BOLD}      4. {color.RED}Uninstall ULTMOS (remove EVERYTHING){color.END}")
    if has_disk_images:
        print(f"{color.END}         Complete removal including {color.RED}all virtual disk images{color.END}\n")
    else:
        print(f"{color.END}         Complete removal of Ultimate macOS KVM repository\n")
    
    print(f"{color.BOLD}      5. {color.BLUE}Clean temporary files{color.END}")
    print(f"{color.END}         Removes all temporary files created during the VM setup process\n")
    
    print(f"{color.END}      Q. Exit\n")
    
    selection = input(f"{color.BOLD}Select> {color.END}")
    return selection

def main():
    # Handle command-line arguments
    if len(sys.argv) > 1:
        force = args.force
        keep_data = args.keepdata
        
        if args.downloads:
            clean_downloaded_images(force)
        elif args.vmonly:
            # Check for both root disk images and disks in the disks/ directory
            remove_vm_data_only(force)
        elif args.tempfiles:
            # Clean temporary files created during VM setup
            clean_temporary_files(force)
        else:
            # Default action is to uninstall
            uninstall_ultimate_macos_kvm(force, keep_data)
    
    # Interactive menu if no arguments are passed
    else:
        while True:
            selection = show_menu()
            
            if selection == "1":
                clear()
                clean_downloaded_images()
                print("\nPress Enter to continue...")
                input()
            
            elif selection == "2":
                clear()
                # Check for disk images in the root directory
                root_disk_images = check_root_disk_images()
                
                # Handle these images before proceeding with VM removal
                if root_disk_images and not handle_root_disk_images(root_disk_images, False):
                    print(f"\n{color.YELLOW}VM data removal cancelled.{color.END}")
                    print("\nPress Enter to continue...")
                    input()
                    continue
                    
                # Proceed with regular VM data removal    
                remove_vm_data_only(False)
                print("\nPress Enter to continue...")
                input()
            
            elif selection == "3":
                clear()
                # Check for disk images in the root directory to ensure they're backed up
                root_disk_images = check_root_disk_images()
                if root_disk_images:
                    print(f"\n{color.YELLOW}Found disk images in root directory.{color.END}")
                    print(f"{color.YELLOW}These will be included in the backup before uninstallation.{color.END}")
                    
                uninstall_ultimate_macos_kvm(False, True)  # Keep user data
            
            elif selection == "4":
                clear()
                # Check for disk images in the root directory
                root_disk_images = check_root_disk_images()
                if root_disk_images:
                    print(f"\n{color.RED}WARNING: Found disk images in root directory.{color.END}")
                    print(f"{color.RED}These will be PERMANENTLY DELETED along with everything else!{color.END}")
                    
                uninstall_ultimate_macos_kvm(False, False)  # Remove everything
            
            elif selection == "5":
                clear()
                clean_temporary_files(False)
                print("\nPress Enter to continue...")
                input()
            
            elif selection.lower() == "q":
                break
            
            else:
                clear()
                print(f"\n{color.RED}Invalid selection. Please try again.{color.END}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n{color.YELLOW}Operation cancelled by user.{color.END}")
        sys.exit(0)

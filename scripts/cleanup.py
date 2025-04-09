#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

import os
import time
import subprocess
import json
import sys
import argparse
import shutil
import tempfile
from datetime import datetime
sys.path.append('./resources/python')
from cpydColours import color

# Check if we're in the correct directory
if not os.path.exists("./main.py"):
    print("Error: This script must be run from the root of the Ultimate macOS KVM directory.")
    sys.exit(1)

script = "cleanup.py"
scriptName = "Ultimate macOS KVM Uninstaller"
scriptID = "UNINST"
scriptVendor = "Coopydood"

# Parse command line arguments
parser = argparse.ArgumentParser("Uninstaller for Ultimate macOS KVM")
parser.add_argument("--downloads", dest="downloads", help="Clean downloaded recovery images", action="store_true")
parser.add_argument("--force", dest="force", help="Force uninstallation without confirmation", action="store_true")
parser.add_argument("--keep-data", dest="keepdata", help="Keep user data during uninstallation", action="store_true")
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
        
    # List all domains from virsh
    try:
        result = subprocess.run(['virsh', 'list', '--all', '--name'], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        vm_list = result.stdout.strip().split('\n')
        
        # Filter for Ultimate macOS KVM VMs
        ultmos_vms = []
        for vm in vm_list:
            vm = vm.strip()
            if not vm:  # Skip empty lines
                continue
                
            # Check if this is an Ultimate macOS KVM VM by examining its XML definition
            try:
                xml_result = subprocess.run(['virsh', 'dumpxml', vm], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
        
        if ultmos_vms:
            print(f"  {color.YELLOW}Found {len(ultmos_vms)} Ultimate macOS KVM VM(s) in virt-manager:{color.END}")
            for vm in ultmos_vms:
                print(f"  - {vm}")
        else:
            print(f"  {color.GREEN}No Ultimate macOS KVM VMs found in virt-manager.{color.END}")
            
        return ultmos_vms
        
    except Exception as e:
        print(f"  {color.YELLOW}Error checking for virt-manager VMs: {str(e)}{color.END}")
        return []

def remove_virtmanager_vms(vm_list):
    """Remove Ultimate macOS KVM VMs from virt-manager"""
    if not vm_list:
        return True
        
    print(f"\n{color.BOLD}{color.YELLOW}Removing Ultimate macOS KVM VMs from virt-manager...{color.END}")
    
    success = True
    for vm in vm_list:
        try:
            # Try to destroy the VM first (if running)
            subprocess.run(['virsh', 'destroy', vm], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
            # Undefine the VM with storage
            result = subprocess.run(['virsh', 'undefine', vm, '--remove-all-storage'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                print(f"  {color.GREEN}✓{color.END} Removed VM: {vm}")
            else:
                # Try without storage removal as fallback
                result = subprocess.run(['virsh', 'undefine', vm], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    print(f"  {color.GREEN}✓{color.END} Removed VM (storage may remain): {vm}")
                else:
                    print(f"  {color.RED}✗{color.END} Failed to remove VM: {vm}")
                    success = False
        except Exception as e:
            print(f"  {color.RED}✗{color.END} Error removing VM {vm}: {str(e)}")
            success = False
            
    return success

def create_self_destruct_script(directory, keep_user_data=False, virt_vms=None):
    """Create a temporary script that will delete the Ultimate macOS KVM directory after this script terminates"""
    # Create a temp file for our self-destruct script
    fd, path = tempfile.mkstemp(suffix='.sh')
    try:
        user_data_dir = os.path.join(directory, "disks")
        
        script_content = f"""#!/bin/bash
# Wait for the parent process to exit
sleep 2

echo "Removing Ultimate macOS KVM directory: {directory}"
"""
        
        # Add virsh VM removal if needed
        if virt_vms:
            script_content += f"""
# Removing related VMs from virt-manager
echo "Removing Ultimate macOS KVM VMs from virt-manager..."
"""
            for vm in virt_vms:
                script_content += f"""
virsh destroy "{vm}" 2>/dev/null
virsh undefine "{vm}" --remove-all-storage 2>/dev/null || virsh undefine "{vm}" 2>/dev/null
"""
        
        # If we're keeping user data, move it to a temp location first
        if keep_user_data and os.path.exists(user_data_dir):
            temp_backup_dir = os.path.expanduser("~/ultmos_user_data_backup")
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
    print(f"\n{color.BOLD}{color.RED}UNINSTALLING Ultimate macOS KVM...{color.END}")
    
    # Serious warning
    print(f"\n{color.BOLD}{color.RED}WARNING: THIS WILL COMPLETELY REMOVE Ultimate macOS KVM!{color.END}")
    print(f"{color.YELLOW}This is a permanent operation that will:{color.END}")
    print(f"  - Delete ALL Ultimate macOS KVM files, scripts, and configurations")
    print(f"  - Remove all downloaded macOS images")
    
    if keep_data:
        print(f"\n{color.GREEN}User data (virtual disks) will be backed up to your home directory.{color.END}")
    else:
        print(f"  - {color.RED}DELETE ALL YOUR VIRTUAL DISK IMAGES{color.END}")
    
    # Check for VMs in virt-manager
    virt_vms = check_virtmanager_vms()
    if virt_vms:
        print(f"\n{color.RED}WARNING: Found Ultimate macOS KVM VMs in virt-manager!{color.END}")
        print(f"These will also be removed during uninstallation.")
    
    # Confirmation - require typing "UNINSTALL" to proceed
    if not force:
        print(f"\n{color.BOLD}This action cannot be undone. Type {color.RED}UNINSTALL{color.END}{color.BOLD} to proceed or anything else to cancel: {color.END}")
        confirmation = input()
        if confirmation != "UNINSTALL":
            print(f"\n{color.YELLOW}Uninstallation cancelled.{color.END}")
            return 0
        
        # If VMs were found, ask for specific confirmation
        if virt_vms and not force:
            print(f"\n{color.YELLOW}Do you want to remove the Ultimate macOS KVM VMs from virt-manager? (y/n): {color.END}")
            vm_confirmation = input()
            if vm_confirmation.lower() not in ['y', 'yes']:
                print(f"  {color.YELLOW}VMs will be kept in virt-manager.{color.END}")
                virt_vms = []
    
    # Check and unmount any mounted images
    if not check_mounted_images():
        print(f"\n{color.YELLOW}Warning: Some files may be in use and cannot be deleted.{color.END}")
        if not force:
            print(f"Use --force to attempt deletion anyway.")
            return 0
    
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
    print(f"\n\n   {color.BOLD}{color.RED}Ultimate macOS KVM UNINSTALLER{color.END}")
    print(f"   Ultimate macOS KVM v{version}\n")
    print(f"   This tool allows you to clean up or completely remove Ultimate macOS KVM\n")
    
    print(f"{color.BOLD}      1. Clean downloaded macOS images")
    print(f"{color.END}         Removes downloaded recovery and installation files\n")
    
    print(f"{color.BOLD}      2. {color.RED}Uninstall Ultimate macOS KVM (keep virtual disks){color.END}")
    print(f"{color.END}         Completely removes Ultimate macOS KVM but backs up your VM disk images\n")
    
    print(f"{color.BOLD}      3. {color.RED}Uninstall Ultimate macOS KVM (remove EVERYTHING){color.END}")
    print(f"{color.END}         Complete removal including all virtual disk images\n")
    
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
                uninstall_ultimate_macos_kvm(False, True)  # Keep user data
            
            elif selection == "3":
                clear()
                uninstall_ultimate_macos_kvm(False, False)  # Remove everything
            
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

#!/usr/bin/env python3

"""
Ultimate macOS KVM Uninstaller and Cleanup Utility

This script was created by kunihir0
https://github.com/kunihir0
https://github.com/Coopydood/ultimate-macOS-KVM
"""

import os
import sys
import time
import argparse
from typing import Dict, List, Optional

# Import our utility modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Define the fallback function to check if we're in the correct directory
def check_correct_directory():
    """Check if we're in the correct directory"""
    return os.path.exists("./main.py")

# Try to import utility modules with fallbacks
# Import temp file cleaning functions
try:
    from utils.remove_temp import clean_logs, clean_main_directory, clean_blobs_directory, clean_resources
    has_basic_temp_utils = True
except ImportError as e:
    print(f"Warning: Could not import basic temp cleaning utilities: {str(e)}")
    has_basic_temp_utils = False

# Try to import extended temp cleaning functions
try:
    from utils.remove_temp import clean_pycache, clean_script_store, clean_boot_files, clean_ovmf_files
    has_extended_temp_utils = True
except ImportError as e:
    print(f"Note: Extended temp cleaning functions not available, will use basic cleaning only")
    has_extended_temp_utils = False
    
# Import VM utilities
try:
    from utils.vm_utils import (
        check_virtmanager_vms,
        remove_virtmanager_vms,
        check_running_vms,
        stop_running_vms,
        check_mounted_images
    )
    has_vm_utils = True
except ImportError as e:
    print(f"Warning: Could not import VM utilities: {str(e)}")
    has_vm_utils = False
    
# Import disk utilities
try:
    from utils.disk_utils import (
        check_root_disk_images,
        handle_root_disk_images,
        clean_disk_directory,
        clean_downloaded_images
    )
    has_disk_utils = True
except ImportError as e:
    print(f"Warning: Could not import disk utilities: {str(e)}")
    has_disk_utils = False
    
# Import uninstaller utilities
try:
    from utils.uninstaller_utils import (
        create_self_destruct_script,
        execute_self_destruct,
        check_for_version,
        get_project_root,
        ask_confirmation
    )
    has_uninstaller_utils = True
except ImportError as e:
    print(f"Warning: Could not import uninstaller utilities: {str(e)}")
    has_uninstaller_utils = False

# Add the correct path to find the cpydColours module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'python')))

# Define fallback color class in case import fails
class Colors:
    """ANSI color codes for terminal output"""
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
    # Using the fallback color class
    color = Colors


# Script information
SCRIPT_INFO = {
    "name": "Ultimate macOS KVM Uninstaller",
    "id": "UNINST",
    "vendor": "kunihir0"
}


class UMKUninstaller:
    """Main class for the Ultimate macOS KVM uninstaller and cleanup utility"""
    
    def __init__(self, force: bool = False, keep_data: bool = False):
        """Initialize the uninstaller
        
        Args:
            force: If True, skip confirmations
            keep_data: If True, keep user data during uninstallation
        """
        self.force = force
        self.keep_data = keep_data
        
        # Check if we're in the correct directory
        if not os.path.exists("./main.py"):
            print(f"{color.RED}Error: This script must be run from the root of the Ultimate macOS KVM directory.{color.END}")
            sys.exit(1)
            
        # Try to get version
        try:
            if 'check_for_version' in globals():
                self.version = check_for_version()
            else:
                # Fallback version check
                try:
                    with open("./.version", "r") as f:
                        self.version = f.read().strip()
                except:
                    self.version = "Unknown"
        except Exception:
            self.version = "Unknown"
    
    def clear_screen(self):
        """Clear the terminal screen"""
        print("\n" * 150)
        
    def log(self, message: str, level: str = "info", indent: int = 0, bold: bool = False, end: str = "\n"):
        """Print a formatted log message
        
        Args:
            message: The message to print
            level: Log level (info, success, warning, error)
            indent: Indentation level (number of spaces to prepend)
            bold: Whether to make the text bold
            end: String appended after the end of the message
        """
        # Set color based on level
        log_color = color.END
        if level == "success":
            log_color = color.GREEN
        elif level == "warning":
            log_color = color.YELLOW
        elif level == "error":
            log_color = color.RED
        elif level == "info-blue":
            log_color = color.BLUE
            
        # Apply indent
        indent_str = " " * indent
        prefix = f"{indent_str}"
        
        # Apply formatting
        if bold:
            prefix += color.BOLD
        
        # Special prefixes for some levels
        if level == "success":
            prefix += f"{color.GREEN}✓{color.END} "
        elif level == "error":
            prefix += f"{color.RED}✗{color.END} "
            
        # Print the message
        if bold and level != "info":
            print(f"{prefix}{color.BOLD}{log_color}{message}{color.END}", end=end)
        else:
            print(f"{prefix}{log_color}{message}{color.END}", end=end)
    
    def clean_temporary_files(self) -> int:
        """Clean temporary files using the remove_temp.py utility
        
        Returns:
            int: Number of files cleaned
        """
        self.log("Cleaning temporary files...", "info-blue", bold=True)
        
        # Check if we have the imported functions from remove_temp.py
        required_functions = [
            'clean_logs', 'clean_main_directory', 'clean_blobs_directory', 
            'clean_resources', 'clean_pycache', 'clean_script_store', 
            'clean_boot_files', 'clean_ovmf_files'
        ]
        
        missing_functions = [f for f in required_functions if f not in globals()]
        if missing_functions:
            self.log(f"Some remove_temp.py functions are not available: {', '.join(missing_functions)}", "warning", indent=2)
            self.log(f"Cleanup may be incomplete. Consider updating your installation.", "warning", indent=2)
            
            # Check if we have the essential functions at least
            essential_functions = ['clean_logs', 'clean_main_directory', 'clean_blobs_directory', 'clean_resources']
            missing_essential = [f for f in essential_functions if f not in globals()]
            if missing_essential:
                self.log(f"Essential cleanup functions are missing. Skipping temporary file cleanup.", "error", indent=2)
                return 0
        
        # Confirmation
        if not self.force:
            self.log("This will remove all temporary files created during the VM setup process.", indent=2)
            confirmation = ask_confirmation("Continue with cleaning temporary files?", force=self.force)
            if not confirmation:
                self.log("Skipped cleaning temporary files.", "warning", indent=2)
                return 0
        
        # Use the imported functions from remove_temp.py
        total_removed = 0
        try:
            # Core cleanup functions
            if has_basic_temp_utils:
                self.log("Cleaning log files...", "info-blue", indent=2)
                total_removed += clean_logs()
                
                self.log("Cleaning main directory...", "info-blue", indent=2)
                total_removed += clean_main_directory()
                
                self.log("Cleaning blob files...", "info-blue", indent=2)
                total_removed += clean_blobs_directory()
                
                self.log("Cleaning resource files...", "info-blue", indent=2)
                total_removed += clean_resources()
            
            # Extended cleanup functions (new)
            if has_extended_temp_utils:
                try:
                    self.log("Cleaning Python bytecode files...", "info-blue", indent=2)
                    total_removed += clean_pycache()
                    
                    self.log("Cleaning script store files...", "info-blue", indent=2)
                    total_removed += clean_script_store()
                    
                    self.log("Cleaning boot files...", "info-blue", indent=2)
                    total_removed += clean_boot_files()
                    
                    self.log("Cleaning OVMF files...", "info-blue", indent=2)
                    total_removed += clean_ovmf_files()
                except Exception as e:
                    self.log(f"Error during extended cleanup: {str(e)}", "warning", indent=2)
            
            self.log(f"Successfully cleaned {total_removed} temporary files.", "success", indent=2)
        except Exception as e:
            self.log(f"Error during temp file cleanup: {str(e)}", "error", indent=2)
            return 0
        
        return total_removed
    
    def remove_vm_data_only(self) -> bool:
        """Remove VM and VM data without uninstalling ULTMOS repository
        
        Returns:
            bool: True if removal was successful, False otherwise
        """
        self.log("REMOVING VM AND VM DATA ONLY", "info-blue", bold=True)
        
        # Warning
        self.log("WARNING: This will remove VMs and VM data only", "warning", bold=True)
        self.log("This operation will:", "warning")
        self.log("- Remove VMs from virt-manager if found", indent=2)
        self.log("- Delete all VM disk images in the disks/ directory", indent=2)
        self.log("- Handle any disk images in the root directory", indent=2)
        self.log("- Keep the ULTMOS repository intact", indent=2)
        
        # Check for VMs in virt-manager
        if has_vm_utils:
            virt_vms = check_virtmanager_vms(log_func=self.log)
        else:
            self.log("VM utilities not available, skipping VM checks", "warning")
            virt_vms = []
        
        # Check for running QEMU processes
        if has_vm_utils:
            running_vms = check_running_vms(log_func=self.log)
        else:
            running_vms = []
        
        # Check for root directory disk images
        if has_disk_utils:
            root_disk_images = check_root_disk_images(log_func=self.log)
        else:
            self.log("Disk utilities not available, skipping disk image checks", "warning")
            root_disk_images = []
        
        # Confirmation
        if not self.force:
            confirmation = ask_confirmation("", "REMOVE-VM", self.force)
            if not confirmation:
                self.log("VM removal cancelled.", "warning")
                return False
        
        # Remove VMs from virt-manager if found
        if virt_vms:
            if not self.force:
                vm_confirmation = ask_confirmation("Do you want to remove the ULTMOS VMs from virt-manager?", 
                                                force=self.force)
                if vm_confirmation:
                    remove_virtmanager_vms(virt_vms, log_func=self.log)
                else:
                    self.log("VMs will be kept in virt-manager.", "warning", indent=2)
            else:
                # Force removal of VMs
                remove_virtmanager_vms(virt_vms, log_func=self.log)
        
        # Stop running QEMU processes
        if running_vms:
            stop_running_vms(running_vms, self.force, log_func=self.log)
        
        # Handle root disk images
        if root_disk_images:
            handle_root_disk_images(root_disk_images, self.force, log_func=self.log)
        
        # Check and unmount any mounted images
        check_mounted_images(log_func=self.log)
        
        # Clean disk directory
        return clean_disk_directory(self.force, log_func=self.log)
    
    def uninstall_ultimate_macos_kvm(self) -> int:
        """Complete self-destructing uninstallation of Ultimate macOS KVM
        
        Returns:
            int: 0 if uninstallation failed, 1 if successful
        """
        self.log("UNINSTALLING ULTMOS...", "error", bold=True)
        
        # Serious warning
        self.log("WARNING: THIS WILL COMPLETELY REMOVE Ultimate macOS KVM!", "error", bold=True)
        self.log("This is a permanent operation that will:", "warning")
        self.log("- Delete ALL ULTMOS files, scripts, and configurations", indent=2)
        self.log("- Remove all downloaded macOS images", indent=2)
        
        if self.keep_data:
            self.log("User data (virtual disks) will be backed up to your home directory.", "success")
        else:
            self.log("- DELETE ALL YOUR VIRTUAL DISK IMAGES", "error", indent=2)
        
        # Check for VMs in virt-manager
        virt_vms = check_virtmanager_vms(log_func=self.log)
        if virt_vms:
            self.log("WARNING: Found ULTMOS VMs in virt-manager!", "error")
            self.log("These will also be removed during uninstallation.")
        
        # Check for running QEMU processes
        running_vms = check_running_vms(log_func=self.log)
        if running_vms:
            self.log("WARNING: Found running macOS VMs started directly!", "error")
            self.log("These will also be stopped during uninstallation.")
        
        # Check for disk images in the root directory
        root_disk_images = check_root_disk_images(log_func=self.log)
        if root_disk_images:
            handle_root_disk_images(root_disk_images, self.force, log_func=self.log)
        
        # Confirmation - require typing "UNINSTALL" to proceed
        if not self.force:
            confirmation = ask_confirmation("This action cannot be undone.", "UNINSTALL", self.force)
            if not confirmation:
                self.log("Uninstallation cancelled.", "warning")
                return 0
            
            # If VMs were found, ask for specific confirmation
            if virt_vms:
                vm_confirmation = ask_confirmation("Do you want to remove the ULTMOS VMs from virt-manager?", 
                                                force=self.force)
                if not vm_confirmation:
                    self.log("VMs will be kept in virt-manager.", "warning", indent=2)
                    virt_vms = []
            
            # If running VMs were found, ask for specific confirmation
            if running_vms:
                running_confirmation = ask_confirmation("Do you want to stop the running macOS VMs?", 
                                                     force=self.force)
                if not running_confirmation:
                    self.log("Running VMs will not be stopped.", "warning", indent=2)
                    running_vms = []
        
        # Check and unmount any mounted images
        if not check_mounted_images(log_func=self.log):
            self.log("Warning: Some files may be in use and cannot be deleted.", "warning")
            if not self.force:
                self.log("Use --force to attempt deletion anyway.")
                return 0
        
        # Stop running QEMU processes
        if running_vms:
            stop_running_vms(running_vms, self.force, log_func=self.log)
        
        # Determine the Ultimate macOS KVM root directory (absolute path)
        ultmos_root = os.path.abspath(".")
        
        # Create the self-destruct script
        self_destruct_script = create_self_destruct_script(ultmos_root, self.keep_data, virt_vms, log_func=self.log)
        if not self_destruct_script:
            self.log("Failed to prepare uninstallation. Cannot continue.", "error")
            return 0
        
        self.log("Uninstallation prepared. Ultimate macOS KVM will now be completely removed.", "success")
        self.log("The uninstallation will proceed as soon as you press Enter.")
        input(f"{color.BOLD}Press Enter to begin uninstallation...{color.END}")
        
        # Execute the self-destruct script
        if execute_self_destruct(self_destruct_script, log_func=self.log):
            # Exit immediately to allow the self-destruct script to do its work
            sys.exit(0)
        return 0
    
    def show_menu(self) -> str:
        """Show the main cleanup menu
        
        Returns:
            str: User's menu selection
        """
        self.clear_screen()
        print(f"\n\n   {color.BOLD}{color.RED}ULTMOS UNINSTALLER{color.END}")
        print(f"   by {color.BOLD}{SCRIPT_INFO['vendor']}{color.END}\n")
        print(f"   This tool allows you to clean up or completely remove Ultimate macOS KVM.\n")
        
        # Check if there are any VM resources to clean up
        has_vms = False
        vms_found = check_virtmanager_vms(log_func=lambda x: None)  # Silent log
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
        has_downloads = os.path.exists("./BaseSystem.dmg") or os.path.exists("./resources/BaseSystem.dmg")
        
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
    
    def run_menu(self):
        """Run the interactive menu"""
        while True:
            selection = self.show_menu()
            
            if selection == "1":
                self.clear_screen()
                clean_downloaded_images(self.force, log_func=self.log)
                print("\nPress Enter to continue...")
                input()
            
            elif selection == "2":
                self.clear_screen()
                # Check for disk images in the root directory
                root_disk_images = check_root_disk_images(log_func=self.log)
                
                # Handle these images before proceeding with VM removal
                if root_disk_images and not handle_root_disk_images(root_disk_images, self.force, log_func=self.log):
                    self.log("VM data removal cancelled.", "warning")
                    print("\nPress Enter to continue...")
                    input()
                    continue
                    
                # Proceed with regular VM data removal
                self.remove_vm_data_only()
                print("\nPress Enter to continue...")
                input()
            
            elif selection == "3":
                self.clear_screen()
                # Check for disk images in the root directory to ensure they're backed up
                root_disk_images = check_root_disk_images(log_func=self.log)
                if root_disk_images:
                    self.log("Found disk images in root directory.", "warning")
                    self.log("These will be included in the backup before uninstallation.", "warning")
                    
                # Set keep_data to True for this operation
                old_keep_data = self.keep_data
                self.keep_data = True
                self.uninstall_ultimate_macos_kvm()
                # Restore original keep_data setting (though we'll exit before this matters)
                self.keep_data = old_keep_data
            
            elif selection == "4":
                self.clear_screen()
                # Check for disk images in the root directory
                root_disk_images = check_root_disk_images(log_func=self.log)
                if root_disk_images:
                    self.log("WARNING: Found disk images in root directory.", "error")
                    self.log("These will be PERMANENTLY DELETED along with everything else!", "error")
                    
                # Set keep_data to False for this operation
                old_keep_data = self.keep_data
                self.keep_data = False
                self.uninstall_ultimate_macos_kvm()
                # Restore original keep_data setting (though we'll exit before this matters)
                self.keep_data = old_keep_data
            
            elif selection == "5":
                self.clear_screen()
                self.clean_temporary_files()
                print("\nPress Enter to continue...")
                input()
            
            elif selection.lower() == "q":
                break
            
            else:
                self.clear_screen()
                self.log("Invalid selection. Please try again.", "error")
                time.sleep(1)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser("Uninstaller for Ultimate macOS KVM")
    parser.add_argument("--downloads", dest="downloads", help="Clean downloaded recovery images", action="store_true")
    parser.add_argument("--force", dest="force", help="Force uninstallation without confirmation", action="store_true")
    parser.add_argument("--keep-data", dest="keepdata", help="Keep user data during uninstallation", action="store_true")
    parser.add_argument("--vm-only", dest="vmonly", help="Remove only VM and VM data, keep repository", action="store_true")
    parser.add_argument("--temp-files", dest="tempfiles", help="Clean temporary files created during VM setup", action="store_true")
    return parser.parse_args()


def main():
    """Main function"""
    # Parse command line arguments
    args = parse_args()
    
    try:
        # Create uninstaller instance
        uninstaller = UMKUninstaller(force=args.force, keep_data=args.keepdata)
        
        # Handle command-line arguments
        if len(sys.argv) > 1:
            if args.downloads:
                if has_disk_utils:
                    clean_downloaded_images(args.force, log_func=uninstaller.log)
                else:
                    print(f"{color.RED}Error: Disk utilities not available, cannot clean downloads{color.END}")
            elif args.vmonly:
                uninstaller.remove_vm_data_only()
            elif args.tempfiles:
                uninstaller.clean_temporary_files()
            else:
                # Default action is to uninstall
                uninstaller.uninstall_ultimate_macos_kvm()
        else:
            # Interactive menu if no arguments are passed
            uninstaller.run_menu()
    except Exception as e:
        print(f"{color.RED}Error: {str(e)}{color.END}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{color.YELLOW}Operation cancelled by user.{color.END}")
        sys.exit(0)

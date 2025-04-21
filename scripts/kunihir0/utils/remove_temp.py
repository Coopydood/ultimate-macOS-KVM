#!/usr/bin/env python3

"""
This script cleans up all temporary and generated files created during the VM setup process.
"""

import os
import sys
import glob
import shutil
from datetime import datetime

def print_header():
    """Print script header"""
    print("\n" + "="*60)
    print(" UMK File Cleanup Utility ".center(60, "="))
    print("="*60)
    print("\nThis script will remove all temporary and generated files\n")

def confirm_action():
    """Ask for confirmation before proceeding"""
    response = input("Are you sure you want to proceed with cleanup? (y/N): ").lower()
    return response in ['y', 'yes']

def delete_file(path):
    """Delete a file and print the result"""
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"✓ Removed: {path}")
            return True
        return False
    except Exception as e:
        print(f"✗ Failed to remove {path}: {str(e)}")
        return False

def delete_files_in_directory(directory, pattern="*"):
    """Delete all files matching the pattern in a directory"""
    try:
        if not os.path.exists(directory):
            return 0
        
        count = 0
        for file_path in glob.glob(os.path.join(directory, pattern)):
            if os.path.isfile(file_path):
                if delete_file(file_path):
                    count += 1
        return count
    except Exception as e:
        print(f"Error cleaning directory {directory}: {str(e)}")
        return 0

def clean_logs():
    """Clean log files"""
    print("\nCleaning log files...")
    count = delete_files_in_directory("logs", "APC_RUN_*.log")
    print(f"Removed {count} log files")
    return count

def clean_main_directory():
    """Clean files in the main directory"""
    print("\nCleaning root directory files...")
    count = 0
    root_files = [
        "BaseSystem.img",
        "boot.sh",
        "HDD.qcow2"
    ]
    
    for file_path in root_files:
        if delete_file(file_path):
            count += 1
    
    print(f"Removed {count} files from root directory")
    return count

def clean_blobs_directory():
    """Clean all APB blob files"""
    print("\nCleaning blob files...")
    
    # Files directly in blobs directory
    count = delete_files_in_directory("blobs", "USR_*.apb")
    
    # Files in stale subdirectory
    count += delete_files_in_directory("blobs/stale", "USR_*.apb")
    
    # Files in user subdirectory
    count += delete_files_in_directory("blobs/user", "USR_*.apb")
    
    print(f"Removed {count} blob files")
    return count

def clean_resources():
    """Clean resource files"""
    print("\nCleaning resource files...")
    count = 0
    
    resource_files = [
        "resources/BaseSystem.dmg",
        "resources/BaseSystem.img"
    ]
    
    for file_path in resource_files:
        if delete_file(file_path):
            count += 1
            
    print(f"Removed {count} resource files")
    return count

def delete_file_list(file_list):
    """Delete a list of specific files"""
    count = 0
    for file_path in file_list:
        if delete_file(file_path):
            count += 1
    return count

def main():
    """Main function"""
    print_header()
    
    # Get root directory of the project
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to project root directory if needed
    if os.path.basename(script_dir) == "scripts":
        os.chdir(os.path.dirname(script_dir))
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("Error: This script must be run from the UMK root directory.")
        return 1
    
    # List all files from the log
    files_to_clean = [
        "logs/APC_RUN_21-04-2025_00-08-41.log",
        
        # Blob files in main blobs directory
        "blobs/USR_CFG.apb",
        "blobs/USR_CPU_CORES.apb",
        "blobs/USR_CPU_THREADS.apb",
        "blobs/USR_TARGET_OS.apb",
        "blobs/USR_TARGET_OS_NAME.apb",
        "blobs/USR_CPU_FEATURE_ARGS.apb",
        "blobs/USR_CPU_MODEL.apb",
        "blobs/USR_ALLOCATED_RAM.apb",
        "blobs/USR_HDD_ISPHYSICAL.apb",
        "blobs/USR_HDD_PATH.apb",
        "blobs/USR_HDD_SIZE.apb",
        "blobs/USR_HDD_TYPE.apb",
        "blobs/USR_NETWORK_DEVICE.apb",
        "blobs/USR_BOOT_FILE.apb",
        "blobs/USR_MAC_ADDRESS.apb",
        "blobs/USR_CREATE_XML.apb",
        "blobs/USR_SCREEN_RES.apb",
        
        # Resource files
        "resources/BaseSystem.dmg",
        "resources/BaseSystem.img",
        
        # Root directory files
        "BaseSystem.img",
        "HDD.qcow2",
        "boot.sh",
        
        # Blob files in stale directory
        "blobs/stale/USR_ALLOCATED_RAM.apb",
        "blobs/stale/USR_BOOT_FILE.apb",
        "blobs/stale/USR_CFG.apb",
        "blobs/stale/USR_CPU_CORES.apb",
        "blobs/stale/USR_CPU_FEATURE_ARGS.apb",
        "blobs/stale/USR_CPU_MODEL.apb",
        "blobs/stale/USR_CPU_THREADS.apb",
        "blobs/stale/USR_CREATE_XML.apb",
        "blobs/stale/USR_HDD_ISPHYSICAL.apb",
        "blobs/stale/USR_HDD_PATH.apb",
        "blobs/stale/USR_HDD_SIZE.apb",
        "blobs/stale/USR_HDD_TYPE.apb",
        "blobs/stale/USR_MAC_ADDRESS.apb",
        "blobs/stale/USR_NETWORK_DEVICE.apb",
        "blobs/stale/USR_SCREEN_RES.apb",
        "blobs/stale/USR_TARGET_OS.apb",
        "blobs/stale/USR_TARGET_OS_NAME.apb",
        
        # Blob files in user directory
        "blobs/user/USR_ALLOCATED_RAM.apb",
        "blobs/user/USR_BOOT_FILE.apb",
        "blobs/user/USR_CFG.apb", 
        "blobs/user/USR_CPU_CORES.apb",
        "blobs/user/USR_CPU_FEATURE_ARGS.apb",
        "blobs/user/USR_CPU_MODEL.apb",
        "blobs/user/USR_CPU_THREADS.apb",
        "blobs/user/USR_CREATE_XML.apb",
        "blobs/user/USR_HDD_ISPHYSICAL.apb",
        "blobs/user/USR_HDD_PATH.apb",
        "blobs/user/USR_HDD_SIZE.apb",
        "blobs/user/USR_HDD_TYPE.apb",
        "blobs/user/USR_MAC_ADDRESS.apb",
        "blobs/user/USR_NETWORK_DEVICE.apb",
        "blobs/user/USR_SCREEN_RES.apb",
        "blobs/user/USR_TARGET_OS.apb",
        "blobs/user/USR_TARGET_OS_NAME.apb"
    ]
    
    # Print summary
    print(f"Found {len(files_to_clean)} files to clean")
    
    # Ask for confirmation
    if not confirm_action():
        print("Cleanup cancelled.")
        return 0
    
    # Cleanup methods approach
    total_removed = 0
    total_removed += clean_logs()
    total_removed += clean_main_directory()
    total_removed += clean_blobs_directory()
    total_removed += clean_resources()
    
    # Verify all files from the log have been cleaned
    print("\nVerifying all files have been cleaned...")
    remaining_files = [f for f in files_to_clean if os.path.exists(f)]
    
    if remaining_files:
        print(f"\nWarning: {len(remaining_files)} files were not cleaned:")
        for file_path in remaining_files:
            print(f"  - {file_path}")
        
        # Try to clean them directly
        print("\nAttempting to clean remaining files directly...")
        additional_removed = delete_file_list(remaining_files)
        total_removed += additional_removed
        
        if additional_removed > 0:
            print(f"Successfully removed an additional {additional_removed} files")
    
    print(f"\nCleanup completed. Removed {total_removed} files in total.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
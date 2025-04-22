#!/usr/bin/env python3

"""
Disk image utilities for the Ultimate macOS KVM project.
Handles disk image detection, cleanup, and management.
"""

import os
import glob
import shutil
from typing import List, Dict, Optional, Any

class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Try to import cpydColours but use our fallback if it fails
try:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'python')))
    from cpydColours import color
except (ImportError, NameError):
    # Using the fallback color class
    color = Colors


# File patterns for detection
DISK_IMAGE_PATTERNS = [
    "*.qcow2",
    "*.img",
    "*.raw",
    "*.vdi",
    "*.vmdk",
    "HDD*"
]

# Root directory filter patterns
ROOT_DIR_FILTERS = [
    "boot/OpenCore.qcow2",
    "BaseSystem.img",
    "/resources/",
    "/boot/"
]


def check_root_disk_images(log_func=print) -> List[str]:
    """Check for disk images in the root directory that might conflict with autopilot
    
    Args:
        log_func: Function to use for logging
        
    Returns:
        List[str]: List of paths to disk images in the root directory
    """
    log_func(f"\n{color.BOLD}{color.BLUE}Checking for disk images in root directory...{color.END}")
    
    root_dir = os.path.abspath(".")
    root_images = []
    
    # Find all disk images in root directory
    for pattern in DISK_IMAGE_PATTERNS:
        matching_files = glob.glob(os.path.join(root_dir, pattern))
        # Filter out known system files like BaseSystem.img and OpenCore.qcow2 in boot/
        filtered_files = [f for f in matching_files if not any(filter_str in f for filter_str in ROOT_DIR_FILTERS)]
        root_images.extend(filtered_files)
    
    # Report findings
    if root_images:
        log_func(f"  {color.YELLOW}Found {len(root_images)} disk images in root directory:{color.END}")
        for img in root_images:
            log_func(f"  - {os.path.basename(img)}")
    else:
        log_func(f"  {color.GREEN}No disk images found in root directory.{color.END}")
        
    return root_images


def handle_root_disk_images(disk_images: List[str], force: bool = False, log_func=print) -> bool:
    """Handle disk images found in the root directory
    
    Args:
        disk_images: List of paths to disk images
        force: Whether to force operations without confirmation
        log_func: Function to use for logging
        
    Returns:
        bool: True if handled successfully, False otherwise
    """
    if not disk_images:
        return True
    
    log_func(f"\n{color.BOLD}{color.YELLOW}Disk images found in root directory need attention{color.END}")
    log_func(f"  These disk images may conflict with autopilot if you reinstall.")
    
    # Present options
    if not force:
        log_func(f"\n  {color.BOLD}What would you like to do?{color.END}")
        log_func(f"  1. Move to 'disks/' directory (recommended)")
        log_func(f"  2. Delete disk images")
        log_func(f"  3. Keep as is (may cause conflicts with autopilot)")
        
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
                    log_func(f"  {color.YELLOW}Warning: {disk_name} already exists in disks/{color.END}")
                    overwrite = input(f"  Overwrite? (y/n): ")
                    if overwrite.lower() not in ['y', 'yes']:
                        log_func(f"  {color.YELLOW}Skipping {disk_name}{color.END}")
                        continue
                
                try:
                    log_func(f"  Moving {disk_name} to disks/ directory...")
                    shutil.move(disk_path, target_path)
                    log_func(f"  {color.GREEN}✓{color.END} Successfully moved {disk_name}")
                except Exception as e:
                    log_func(f"  {color.RED}✗{color.END} Failed to move {disk_name}: {str(e)}")
            
            return True
            
        elif choice == "2":
            # Delete confirmation
            log_func(f"\n  {color.RED}WARNING: This will permanently delete the disk images.{color.END}")
            confirm = input(f"  {color.BOLD}Type 'DELETE' to confirm: {color.END}")
            
            if confirm != "DELETE":
                log_func(f"  {color.YELLOW}Deletion cancelled.{color.END}")
                return False
                
            # Delete each file
            for disk_path in disk_images:
                try:
                    log_func(f"  Deleting {os.path.basename(disk_path)}...")
                    os.remove(disk_path)
                    log_func(f"  {color.GREEN}✓{color.END} Successfully deleted {os.path.basename(disk_path)}")
                except Exception as e:
                    log_func(f"  {color.RED}✗{color.END} Failed to delete {os.path.basename(disk_path)}: {str(e)}")
            
            return True
            
        elif choice == "3":
            log_func(f"\n  {color.YELLOW}Keeping disk images in root directory.{color.END}")
            log_func(f"  {color.YELLOW}Note: This may cause conflicts if you run autopilot again.{color.END}")
            return True
            
        else:
            log_func(f"\n  {color.RED}Invalid choice. Keeping disk images as is.{color.END}")
            return False
    else:
        # In force mode, move to disks/
        disks_dir = os.path.join(os.path.abspath("."), "disks")
        os.makedirs(disks_dir, exist_ok=True)
        
        for disk_path in disk_images:
            try:
                disk_name = os.path.basename(disk_path)
                target_path = os.path.join(disks_dir, disk_name)
                log_func(f"  Moving {disk_name} to disks/ directory...")
                
                # Handle existing files in force mode by overwriting
                if os.path.exists(target_path):
                    os.remove(target_path)
                
                shutil.move(disk_path, target_path)
                log_func(f"  {color.GREEN}✓{color.END} Successfully moved {disk_name}")
            except Exception as e:
                log_func(f"  {color.RED}✗{color.END} Failed to handle {os.path.basename(disk_path)}: {str(e)}")
        
        return True


def clean_disk_directory(force: bool = False, log_func=print) -> bool:
    """Clean the disks directory
    
    Args:
        force: Whether to force operations without confirmation
        log_func: Function to use for logging
        
    Returns:
        bool: True if cleaning was successful, False otherwise
    """
    disks_dir = os.path.join(os.path.abspath("."), "disks")
    if os.path.exists(disks_dir):
        try:
            log_func(f"\n{color.BOLD}Removing VM disk images...{color.END}")
            # List all files to be deleted
            files_found = False
            for root, dirs, files in os.walk(disks_dir):
                for file in files:
                    files_found = True
                    file_path = os.path.join(root, file)
                    log_func(f"  Removing: {file_path}")
            
            if not files_found:
                log_func(f"  {color.YELLOW}No files found in disks directory.{color.END}")
                
            # Actually remove the directory
            shutil.rmtree(disks_dir)
            log_func(f"\n{color.GREEN}✓{color.END} Successfully removed all VM disk images.")
            
            # Create an empty disks directory to maintain project structure
            os.makedirs(disks_dir, exist_ok=True)
            log_func(f"  {color.GREEN}✓{color.END} Created empty disks directory.")
            
            return True
        except Exception as e:
            log_func(f"\n{color.RED}Error removing VM disk images: {str(e)}{color.END}")
            return False
    else:
        log_func(f"\n{color.YELLOW}No VM disk directory found.{color.END}")
        log_func(f"  {color.BLUE}Creating disks directory to maintain project structure...{color.END}")
        
        try:
            os.makedirs(disks_dir, exist_ok=True)
            log_func(f"  {color.GREEN}✓{color.END} Created empty disks directory.")
            return True
        except Exception as e:
            log_func(f"  {color.RED}✗{color.END} Failed to create disks directory: {str(e)}")
            return False


def clean_downloaded_images(force: bool = False, log_func=print) -> int:
    """Clean downloaded macOS recovery images
    
    Args:
        force: Whether to force operations without confirmation
        log_func: Function to use for logging
        
    Returns:
        int: Number of files cleaned
    """
    # Download file patterns
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
    
    log_func(f"\n{color.BOLD}{color.BLUE}Cleaning downloaded recovery images...{color.END}")
    
    # Count downloads
    download_count = 0
    for file_pattern in download_files:
        if "*" in file_pattern:
            matching_files = glob.glob(file_pattern)
            download_count += len(matching_files)
        elif os.path.exists(file_pattern):
            download_count += 1
    
    if download_count == 0:
        log_func(f"  {color.YELLOW}No downloaded recovery images found to clean.{color.END}")
        return 0
    
    # Confirmation
    if not force:
        log_func(f"  Found {download_count} downloaded macOS recovery images to clean.")
        confirmation = input(f"  {color.BOLD}Continue with cleaning downloaded recovery images? (y/n): {color.END}")
        if confirmation.lower() not in ['y', 'yes']:
            log_func(f"  {color.YELLOW}Skipped cleaning downloaded recovery images.{color.END}")
            return 0
    
    # Clean downloads
    cleaned_count = 0
    for file_pattern in download_files:
        if "*" in file_pattern:
            matching_files = glob.glob(file_pattern)
            for file_path in matching_files:
                try:
                    os.remove(file_path)
                    log_func(f"  {color.GREEN}✓{color.END} Removed: {file_path}")
                    cleaned_count += 1
                except Exception as e:
                    log_func(f"  {color.RED}✗{color.END} Failed to remove {file_path}: {str(e)}")
        elif os.path.exists(file_pattern):
            try:
                os.remove(file_pattern)
                log_func(f"  {color.GREEN}✓{color.END} Removed: {file_pattern}")
                cleaned_count += 1
            except Exception as e:
                log_func(f"  {color.RED}✗{color.END} Failed to remove {file_pattern}: {str(e)}")
    
    log_func(f"  {color.GREEN}Cleaned {cleaned_count} downloaded recovery images.{color.END}")
    return cleaned_count
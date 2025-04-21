#!/usr/bin/env python3

"""
Visual cleanup script for Ultimate macOS KVM uninstallation.
This script provides a visually appealing terminal interface for the uninstallation process.
"""

import os
import sys
import time
import shutil
import argparse
import subprocess
from typing import List, Dict, Optional

# ANSI color codes
class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    PURPLE = '\033[95m'
    GRAY = '\u001b[38;5;245m'

# Unicode for progress bars and spinners
BLOCK_FULL = "█"
BLOCK_LIGHT = "░"
SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

def clear_screen():
    """Clear the terminal screen"""
    print("\033c", end="")

def get_terminal_size():
    """Get the terminal size"""
    try:
        columns, rows = shutil.get_terminal_size()
        return columns, rows
    except:
        return 80, 24  # Default size

def print_centered(text: str, color: str = Colors.END):
    """Print text centered in the terminal"""
    columns, _ = get_terminal_size()
    padding = max(0, (columns - len(text.replace("\033[", "").replace("m", ""))) // 2)
    print(" " * padding + color + text + Colors.END)

def print_banner():
    """Print a visually appealing banner"""
    clear_screen()
    columns, _ = get_terminal_size()
    
    print("\n")
    print_centered("╭" + "─" * (columns - 20) + "╮", Colors.RED + Colors.BOLD)
    print("\n")
    print_centered("ULTIMATE macOS KVM", Colors.RED + Colors.BOLD)
    print_centered("UNINSTALLATION PROCESS", Colors.RED + Colors.BOLD)
    print("\n")
    print_centered("╰" + "─" * (columns - 20) + "╯", Colors.RED + Colors.BOLD)
    print("\n")

def progress_bar(progress: float, label: str = "", width: int = 40):
    """Display a progress bar
    
    Args:
        progress: Progress value from 0.0 to 1.0
        label: Text to display next to the progress bar
        width: Width of the progress bar in characters
    """
    columns, _ = get_terminal_size()
    bar_width = min(width, columns - 20)
    
    filled_length = int(bar_width * progress)
    bar = BLOCK_FULL * filled_length + BLOCK_LIGHT * (bar_width - filled_length)
    percent = int(100 * progress)
    
    # Center the progress bar
    padding = max(0, (columns - (bar_width + 10 + len(label))) // 2)
    
    sys.stdout.write("\r" + " " * padding + f"{label} [{bar}] {percent}%")
    sys.stdout.flush()
    
    if progress >= 1:
        sys.stdout.write("\n")
        
def spinner(text: str, seconds: float = 0.1):
    """Display an animated spinner with text
    
    Args:
        text: Text to display next to spinner
        seconds: Time to show spinner animation (in seconds)
    """
    start_time = time.time()
    i = 0
    while time.time() - start_time < seconds:
        spinner_char = SPINNER_CHARS[i % len(SPINNER_CHARS)]
        sys.stdout.write(f"\r{Colors.CYAN}{spinner_char}{Colors.END} {text}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
    sys.stdout.flush()

def print_step(step: str, status: str = ""):
    """Print a step in the uninstallation process
    
    Args:
        step: Step description
        status: Status indicator (success, fail, etc.)
    """
    status_color = Colors.END
    status_symbol = ""
    
    if status == "success":
        status_color = Colors.GREEN
        status_symbol = "✓"
    elif status == "fail":
        status_color = Colors.RED
        status_symbol = "✗"
    elif status == "warning":
        status_color = Colors.YELLOW
        status_symbol = "!"
    
    columns, _ = get_terminal_size()
    padding = max(0, (columns - (len(step) + 4)) // 2)
    
    if status:
        print(" " * padding + f"{step} {status_color}{status_symbol}{Colors.END}")
    else:
        print(" " * padding + step)

def remove_vms(vm_list: List[str]):
    """Remove VMs from virt-manager
    
    Args:
        vm_list: List of VM names to remove
    """
    print_step("Removing VMs from virt-manager")
    
    for i, vm in enumerate(vm_list):
        spinner(f"Removing VM: {vm}", 1.0)
        progress_bar((i+1) / len(vm_list), "VM Removal", 30)
        
        # Try both with and without sudo
        subprocess.run(["virsh", "destroy", vm], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "virsh", "destroy", vm], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["virsh", "undefine", vm, "--remove-all-storage", "--nvram"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "virsh", "undefine", vm, "--remove-all-storage", "--nvram"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("")
    print_step("VM removal complete", "success")

def backup_user_data(source_dir: str, backup_dir: str):
    """Backup user data
    
    Args:
        source_dir: Source directory (usually the disks directory)
        backup_dir: Backup directory (where to copy the data)
    """
    if not os.path.exists(source_dir):
        print_step("No user data to backup", "warning")
        return
    
    print_step("Backing up user data")
    
    # Count total files for progress tracking
    total_files = sum([len(files) for _, _, files in os.walk(source_dir)])
    
    if total_files == 0:
        print_step("No user data files found", "warning")
        return
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy files with progress tracking
    copied_files = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, source_dir)
            dst_path = os.path.join(backup_dir, rel_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            # Copy the file
            spinner(f"Copying: {rel_path}", 0.1)
            shutil.copy2(src_path, dst_path)
            
            # Update progress
            copied_files += 1
            progress_bar(copied_files / total_files, "Backup Progress", 30)
    
    print("")
    print_step("User data backup complete", "success")
    print_step(f"Backed up to: {backup_dir}")

def remove_directory(directory: str):
    """Remove a directory with visual feedback
    
    Args:
        directory: Directory to remove
    """
    print_step(f"Removing directory: {directory}")
    
    # Count total items for progress tracking
    total_items = sum([len(dirs) + len(files) for _, dirs, files in os.walk(directory, topdown=False)])
    
    if total_items == 0:
        print_step("Directory is already empty", "warning")
        return
    
    # Remove files and directories with progress tracking
    removed_items = 0
    for root, dirs, files in os.walk(directory, topdown=False):
        # Remove files first
        for file in files:
            path = os.path.join(root, file)
            spinner(f"Removing: {os.path.basename(path)}", 0.05)
            try:
                os.unlink(path)
                removed_items += 1
                if removed_items % 5 == 0:  # Update progress every 5 items
                    progress_bar(removed_items / total_items, "Cleanup Progress", 30)
            except Exception as e:
                print_step(f"Failed to remove {path}: {str(e)}", "fail")
        
        # Then remove directories
        for dir in dirs:
            path = os.path.join(root, dir)
            spinner(f"Removing dir: {os.path.basename(path)}", 0.05)
            try:
                os.rmdir(path)
                removed_items += 1
                if removed_items % 5 == 0:  # Update progress every 5 items
                    progress_bar(removed_items / total_items, "Cleanup Progress", 30)
            except Exception as e:
                print_step(f"Failed to remove directory {path}: {str(e)}", "fail")
    
    # Finally remove the root directory
    try:
        os.rmdir(directory)
    except Exception:
        pass
    
    print("")
    print_step("Directory removal complete", "success")

def self_destruct(directory: str, keep_user_data: bool = False, virt_vms: Optional[List[str]] = None):
    """Perform the complete self-destruct operation with visual feedback
    
    Args:
        directory: Ultimate macOS KVM directory to remove
        keep_user_data: Whether to backup user data
        virt_vms: List of VM names to remove from virt-manager
    """
    # Print banner
    print_banner()
    
    # Define the backup directory
    user_data_dir = os.path.join(directory, "disks")
    backup_dir = os.path.expanduser("~/ultmos_user_data_backup")
    
    print_step("Beginning uninstallation process")
    time.sleep(1)
    
    # Remove VMs if needed
    if virt_vms and len(virt_vms) > 0:
        remove_vms(virt_vms)
    
    # Backup user data if requested
    if keep_user_data and os.path.exists(user_data_dir):
        backup_user_data(user_data_dir, backup_dir)
    
    # Remove the directory
    print("")
    print_step("Preparing for final cleanup")
    time.sleep(1)
    remove_directory(directory)
    
    # Final message
    print("\n")
    print_centered("╭" + "─" * 40 + "╮", Colors.GREEN)
    print_centered("Ultimate macOS KVM has been completely uninstalled", Colors.GREEN + Colors.BOLD)
    
    if keep_user_data and os.path.exists(backup_dir):
        print_centered("Your virtual disk images have been backed up to:", Colors.GREEN)
        print_centered(backup_dir, Colors.CYAN)
    
    print_centered("Thank you for using Ultimate macOS KVM!", Colors.GREEN)
    print_centered("╰" + "─" * 40 + "╯", Colors.GREEN)
    print("\n")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser("Visual Cleanup for Ultimate macOS KVM")
    parser.add_argument("--directory", required=True, help="Directory to remove")
    parser.add_argument("--keep-data", action="store_true", help="Keep user data during uninstallation")
    parser.add_argument("--vms", nargs="*", help="List of VM names to remove from virt-manager")
    return parser.parse_args()

def main():
    """Main function"""
    try:
        args = parse_args()
        self_destruct(args.directory, args.keep_data, args.vms)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
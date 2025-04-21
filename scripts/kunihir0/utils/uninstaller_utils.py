#!/usr/bin/env python3

"""
Uninstaller utilities for the Ultimate macOS KVM project.
Handles the creation of self-destruct scripts and uninstallation process.
"""

import os
import sys
import tempfile
import subprocess
from typing import List, Optional, Dict, Any

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
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'python')))
    from cpydColours import color
except (ImportError, NameError):
    # Using the fallback color class
    color = Colors


def create_self_destruct_script(directory: str, keep_user_data: bool = False, virt_vms: Optional[List[str]] = None, 
                               log_func=print) -> Optional[str]:
    """Create a temporary script that will delete the Ultimate macOS KVM directory after this script terminates
    
    Args:
        directory: Directory to delete
        keep_user_data: Whether to backup user data during uninstallation
        virt_vms: List of VM names to remove from virt-manager
        log_func: Function to use for logging
        
    Returns:
        str or None: Path to the self-destruct script, or None if failed
    """
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
        log_func(f"  {color.RED}Failed to create self-destruct script: {str(e)}{color.END}")
        try:
            os.unlink(path)
        except:
            pass
        return None


def execute_self_destruct(script_path: str, log_func=print) -> bool:
    """Execute the self-destruct script
    
    Args:
        script_path: Path to the self-destruct script
        log_func: Function to use for logging
        
    Returns:
        bool: True if script was started successfully, False otherwise
    """
    try:
        subprocess.Popen(['sudo', script_path], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         start_new_session=True)
        log_func(f"\n{color.GREEN}Uninstallation in progress...{color.END}")
        log_func(f"You can close this terminal now. Ultimate macOS KVM is being removed.")
        return True
    except Exception as e:
        log_func(f"\n{color.RED}Failed to start uninstallation: {str(e)}{color.END}")
        # Try to delete the script
        try:
            os.unlink(script_path)
        except:
            pass
        return False


def check_for_version() -> str:
    """Check for ULTMOS version
    
    Returns:
        str: Version string or "Unknown"
    """
    try:
        version_path = os.path.join(os.path.abspath("."), ".version")
        if os.path.exists(version_path):
            with open(version_path, "r") as f:
                return f.read().strip()
    except:
        pass
    
    return "Unknown"


def check_correct_directory() -> bool:
    """Check if we're in the correct directory
    
    Returns:
        bool: True if we're in the correct directory, False otherwise
    """
    return os.path.exists("./main.py")


def get_project_root() -> str:
    """Get the project root directory
    
    Returns:
        str: Path to the project root directory
    """
    # Get root directory of the project
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up from utils directory
    if os.path.basename(os.path.dirname(script_dir)) == "kunihir0":
        return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    elif os.path.basename(script_dir) == "kunihir0":
        return os.path.abspath(os.path.join(script_dir, "..", ".."))
    elif os.path.basename(script_dir) == "scripts":
        return os.path.abspath(os.path.join(script_dir, ".."))
    else:
        return os.path.abspath(".")


def ask_confirmation(prompt: str, required_input: Optional[str] = None, force: bool = False) -> bool:
    """Ask for user confirmation
    
    Args:
        prompt: The prompt to display
        required_input: If provided, user must type exactly this to confirm
        force: Whether to skip confirmation
        
    Returns:
        bool: True if confirmed, False otherwise
    """
    if force:
        return True
        
    if required_input:
        print(f"{prompt} Type {color.YELLOW}{required_input}{color.END} to proceed or anything else to cancel: ", end="")
        confirmation = input()
        return confirmation == required_input
    else:
        print(f"{prompt} (y/n): ", end="")
        confirmation = input().lower()
        return confirmation in ['y', 'yes']
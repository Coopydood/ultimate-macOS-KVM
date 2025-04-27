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
    # Create a temp directory for our visual cleanup script
    temp_dir = tempfile.mkdtemp(prefix='ultmos_uninstall_')
    cleanup_script_path = os.path.join(temp_dir, "visual_cleanup.py")
    
    try:
        # Get path to the visual cleanup module
        current_dir = os.path.dirname(os.path.abspath(__file__))
        source_script_path = os.path.join(current_dir, "visual_cleanup.py")
        
        # Copy the visual cleanup script to the temp directory
        try:
            import shutil
            shutil.copy2(source_script_path, cleanup_script_path)
            os.chmod(cleanup_script_path, 0o755)
            log_func(f"  Prepared visual cleanup script.")
        except Exception as e:
            log_func(f"  {color.YELLOW}Warning: Could not copy visual script: {str(e)}{color.END}")
            log_func(f"  {color.YELLOW}Falling back to basic uninstallation.{color.END}")
            return create_basic_self_destruct_script(directory, keep_user_data, virt_vms, log_func)
        
        # Create the wrapper shell script
        fd, path = tempfile.mkstemp(suffix='.sh')
        
        # Format VM list for command line if provided
        vm_args = ""
        if virt_vms:
            vm_list = " ".join([f'"{vm}"' for vm in virt_vms])
            vm_args = f"--vms {vm_list}"
        
        # Create the shell script that calls our Python script
        script_content = f"""#!/bin/bash
# Wait for the parent process to exit
sleep 2

# Run the visual cleanup script
python3 "{cleanup_script_path}" --directory "{directory}" {vm_args} {"--keep-data" if keep_user_data else ""}

# Clean up the temp directory (self-cleanup)
rm -rf "{temp_dir}"
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
            # Clean up
            if os.path.exists(cleanup_script_path):
                os.unlink(cleanup_script_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass
        return None


def create_basic_self_destruct_script(directory: str, keep_user_data: bool = False, virt_vms: Optional[List[str]] = None,
                               log_func=print) -> Optional[str]:
    """Create a basic shell script for self-destruction (fallback if visual cleanup fails)
    
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

# Safety checks to ensure we're deleting the correct directory
echo "Performing safety checks before removal..."

# Check if directory exists
if [ ! -d "{directory}" ]; then
  echo "Directory {directory} does not exist. Aborting."
  exit 1
fi

# Check if it's a valid Ultimate macOS KVM repository
REQUIRED_FILES=("main.py" "LICENSE" "README.md")
REQUIRED_DIRS=("scripts" "resources")
FILES_FOUND=0
DIRS_FOUND=0

for file in "${{REQUIRED_FILES[@]}}"; do
  if [ -f "{directory}/$file" ]; then
    FILES_FOUND=$((FILES_FOUND + 1))
  fi
done

for dir in "${{REQUIRED_DIRS[@]}}"; do
  if [ -d "{directory}/$dir" ]; then
    DIRS_FOUND=$((DIRS_FOUND + 1))
  fi
done

# Require at least 2 expected files and 1 expected directory
if [ $FILES_FOUND -lt 2 ] || [ $DIRS_FOUND -lt 1 ]; then
  echo "SAFETY CHECK FAILED: {directory} does not appear to be a valid Ultimate macOS KVM repository."
  echo "Uninstallation aborted for your safety."
  exit 1
fi

# Check if it's not a system directory
UNSAFE_PATHS=("/" "/bin" "/boot" "/dev" "/etc" "/home" "/lib" "/lib64" "/media" "/mnt" "/opt" "/proc" "/root" "/run" "/sbin" "/srv" "/sys" "/tmp" "/usr" "/var")

DIR_PATH=$(realpath "{directory}")
for path in "${{UNSAFE_PATHS[@]}}"; do
  if [ "$DIR_PATH" = "$path" ]; then
    echo "SAFETY CHECK FAILED: Cannot delete system directory: $DIR_PATH"
    echo "Uninstallation aborted for your safety."
    exit 1
  fi
done

echo "Safety checks passed - confirmed it's the UMK5 repository"
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
# Remove entire repository at once
echo "Removing entire repository: {directory}"
rm -rf --preserve-root "{directory}"

# Verify removal was successful
if [ -d "{directory}" ]; then
  echo "Warning: Some files/directories may remain."
else
  echo "Ultimate macOS KVM has been completely removed."
fi

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
        log_func(f"\n{color.GREEN}Starting uninstallation with visual feedback...{color.END}")
        log_func(f"You may be prompted for your sudo password.")
        
        # Run the script with sudo but keep stdin, stdout, and stderr open
        # This ensures the user can see and respond to the password prompt
        process = subprocess.Popen(['sudo', script_path])
        
        # Wait briefly to allow the sudo prompt to appear
        import time
        time.sleep(1)
        
        log_func(f"\n{color.GREEN}Uninstallation in progress...{color.END}")
        log_func(f"A visual interface will guide you through the uninstallation.")
        log_func(f"Once you've entered your password (if prompted), the process will begin automatically.")
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
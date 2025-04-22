#!/usr/bin/env python3

"""
VM management utilities for the Ultimate macOS KVM project.
Handles virtual machine detection, management, and cleanup.
"""

import os
import time
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


def check_virtmanager_vms(log_func=print) -> List[str]:
    """Check for Ultimate macOS KVM VMs imported into virt-manager
    
    Args:
        log_func: Function to use for logging
        
    Returns:
        List[str]: List of VM names found
    """
    log_func(f"{color.BOLD}{color.BLUE}Checking for VMs in virt-manager...{color.END}")
    
    # Check if virsh is available
    try:
        result = subprocess.run(['which', 'virsh'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            log_func(f"  {color.YELLOW}virt-manager/virsh not found. Skipping VM check.{color.END}")
            return []
    except Exception:
        log_func(f"  {color.YELLOW}Could not check for virsh. Skipping VM check.{color.END}")
        return []
    
    # Try both user-level and system-level approaches
    ultmos_vms = []
    
    # Try user-level first (no sudo)
    try:
        log_func(f"  {color.BLUE}Checking for VMs at user level...{color.END}")
        result = subprocess.run(['virsh', 'list', '--all', '--name'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            vm_list = result.stdout.strip().split('\n')
            ultmos_vms = process_vm_list(vm_list, False, log_func)  # False = no sudo
    except Exception as e:
        log_func(f"  {color.YELLOW}Error checking for user-level VMs: {str(e)}{color.END}")
    
    # If no VMs found at user level, try system level with sudo
    if not ultmos_vms:
        try:
            log_func(f"  {color.BLUE}Checking for VMs at system level (sudo)...{color.END}")
            result = subprocess.run(['sudo', 'virsh', 'list', '--all', '--name'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                vm_list = result.stdout.strip().split('\n')
                ultmos_vms = process_vm_list(vm_list, True, log_func)  # True = use sudo
        except Exception as e:
            log_func(f"  {color.YELLOW}Error checking for system-level VMs: {str(e)}{color.END}")
    
    # Report findings
    if ultmos_vms:
        log_func(f"  {color.YELLOW}Found {len(ultmos_vms)} ULTMOS VM(s) in virt-manager:{color.END}")
        for vm in ultmos_vms:
            log_func(f"  - {vm}")
    else:
        log_func(f"  {color.GREEN}No ULTMOS VMs found in virt-manager.{color.END}")
    
    return ultmos_vms


def process_vm_list(vm_list: List[str], use_sudo: bool, log_func=print) -> List[str]:
    """Process a list of VMs and filter for ULTMOS VMs
    
    Args:
        vm_list: List of VM names to process
        use_sudo: Whether to use sudo for virsh commands
        log_func: Function to use for logging
        
    Returns:
        List[str]: List of ULTMOS VM names
    """
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


def remove_virtmanager_vms(vm_list: List[str], log_func=print) -> bool:
    """Remove ULTMOS VMs from virt-manager
    
    Args:
        vm_list: List of VM names to remove
        log_func: Function to use for logging
        
    Returns:
        bool: True if all VMs were removed successfully, False otherwise
    """
    if not vm_list:
        return True
        
    log_func(f"\n{color.BOLD}{color.YELLOW}Removing ULTMOS VMs from virt-manager...{color.END}")
    
    success = True
    for vm in vm_list:
        log_func(f"  Attempting to remove VM: {vm}")
        
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
                log_func(f"  Trying {sudo_text}...")
                
                # Try to destroy the VM first (if running)
                destroy_cmd = cmd_prefix + ['virsh', 'destroy', vm]
                subprocess.run(destroy_cmd,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                           
                # Try to undefine VM with NVRAM and storage removal
                undefine_cmd = cmd_prefix + ['virsh', 'undefine', vm, '--remove-all-storage', '--nvram']
                result = subprocess.run(undefine_cmd,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0:
                    log_func(f"  {color.GREEN}✓{color.END} Removed VM: {vm} {sudo_text}")
                    vm_removed = True
                    break
                    
                # Try again without storage removal
                undefine_cmd = cmd_prefix + ['virsh', 'undefine', vm, '--nvram']
                result = subprocess.run(undefine_cmd,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                   
                if result.returncode == 0:
                    log_func(f"  {color.GREEN}✓{color.END} Removed VM (storage may remain): {vm} {sudo_text}")
                    vm_removed = True
                    break
                
                # Try one last time without nvram flag
                undefine_cmd = cmd_prefix + ['virsh', 'undefine', vm]
                result = subprocess.run(undefine_cmd,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                   
                if result.returncode == 0:
                    log_func(f"  {color.GREEN}✓{color.END} Removed VM (nvram may remain): {vm} {sudo_text}")
                    vm_removed = True
                    break
                    
                # If we're on the last attempt (with sudo) and still failing, show error
                if use_sudo:
                    log_func(f"  {color.YELLOW}Failed with error: {result.stderr.strip()}{color.END}")
                
            except Exception as e:
                if use_sudo:  # Only show error on last attempt
                    log_func(f"  {color.RED}✗{color.END} Error removing VM {vm}: {str(e)}")
        
        # Check final removal status
        if not vm_removed:
            log_func(f"  {color.RED}✗{color.END} Failed to remove VM: {vm} after multiple attempts")
            success = False
            
    return success


def check_running_vms(log_func=print) -> List[str]:
    """Check for running QEMU processes that might be Ultimate macOS KVM VMs
    
    Args:
        log_func: Function to use for logging
        
    Returns:
        List[str]: List of PIDs of running VMs
    """
    log_func(f"\n{color.BOLD}{color.BLUE}Checking for running QEMU processes...{color.END}")
    
    try:
        # Look for QEMU processes running macOS VMs (common patterns in cmdline)
        result = subprocess.run(['ps', 'aux'], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                             
        if result.returncode != 0:
            log_func(f"  {color.YELLOW}Unable to check for running processes.{color.END}")
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
                        log_func(f"  {color.YELLOW}Found running QEMU process: PID {pid}{color.END}")
                    except (ValueError, IndexError):
                        pass
        
        if not running_vms:
            log_func(f"  {color.GREEN}No running macOS VMs found.{color.END}")
            
        return running_vms
    except Exception as e:
        log_func(f"  {color.YELLOW}Error checking for running processes: {str(e)}{color.END}")
        return []


def stop_running_vms(pids: List[str], force: bool = False, log_func=print) -> bool:
    """Try to gracefully stop running QEMU processes
    
    Args:
        pids: List of PIDs to stop
        force: Whether to force operations without confirmation
        log_func: Function to use for logging
        
    Returns:
        bool: True if all VMs were stopped successfully, False otherwise
    """
    if not pids:
        return True
        
    log_func(f"\n{color.BOLD}{color.YELLOW}Found running macOS VMs that need to be stopped{color.END}")
    
    # Get confirmation unless forced
    if not force:
        log_func(f"  {color.YELLOW}Running VMs must be stopped to continue.{color.END}")
        confirmation = input(f"  {color.BOLD}Stop running VMs? (y/n): {color.END}")
        if confirmation.lower() not in ['y', 'yes']:
            log_func(f"  {color.YELLOW}Operation cancelled. Please shut down your VMs manually.{color.END}")
            return False
    
    success = True
    for pid in pids:
        try:
            log_func(f"  Trying to gracefully stop VM with PID {pid}...")
            # First try SIGTERM for graceful shutdown
            subprocess.run(['kill', pid], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a bit and check if process is gone
            time.sleep(2)
            if subprocess.run(['ps', '-p', pid], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                log_func(f"  {color.GREEN}✓{color.END} Successfully stopped VM with PID {pid}")
                continue
                
            # If still running, ask before using SIGKILL
            if not force:
                log_func(f"  {color.YELLOW}VM with PID {pid} is still running. Force kill? (y/n): {color.END}")
                force_kill = input()
                if force_kill.lower() not in ['y', 'yes']:
                    log_func(f"  {color.YELLOW}VM with PID {pid} was not stopped.{color.END}")
                    success = False
                    continue
            
            # Force kill with SIGKILL
            subprocess.run(['kill', '-9', pid], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(1)
            
            if subprocess.run(['ps', '-p', pid], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                log_func(f"  {color.GREEN}✓{color.END} Successfully force-killed VM with PID {pid}")
            else:
                log_func(f"  {color.RED}✗{color.END} Failed to stop VM with PID {pid}")
                success = False
        except Exception as e:
            log_func(f"  {color.RED}✗{color.END} Error stopping VM with PID {pid}: {str(e)}")
            success = False
    
    return success


def check_mounted_images(log_func=print) -> bool:
    """Check for mounted qcow2 images and try to unmount them
    
    Args:
        log_func: Function to use for logging
        
    Returns:
        bool: True if unmounting succeeded or no mounted images found,
             False if unmounting failed
    """
    log_func(f"\n{color.BOLD}{color.BLUE}Checking for mounted images...{color.END}")
    
    # Check for mounted NBD devices (commonly used for qcow2 mounting)
    try:
        result = subprocess.run(['sudo', 'lsof', '+c', '0', '/dev/nbd*'], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "OpenCore.qcow2" in result.stdout or "BaseSystem.img" in result.stdout:
            log_func(f"  {color.YELLOW}Found mounted qcow2 images. Attempting to unmount...{color.END}")
            
            # Try to unmount using the nbdassistant script if it exists
            if os.path.exists("./scripts/hyperchromiac/nbdassistant.py"):
                subprocess.run(['sudo', './scripts/hyperchromiac/nbdassistant.py', '-u', '-q'], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                log_func(f"  {color.GREEN}✓{color.END} Unmounted qcow2 images.")
            else:
                log_func(f"  {color.YELLOW}NBD unmount script not found. Some files may be locked.{color.END}")
                return False
            return True
    except Exception as e:
        log_func(f"  {color.YELLOW}Warning: Could not check for mounted images: {str(e)}{color.END}")
    
    return True
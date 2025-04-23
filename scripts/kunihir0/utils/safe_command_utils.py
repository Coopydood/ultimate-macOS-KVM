#!/usr/bin/env python3

"""
Safe command execution utilities for kunihir0 that follow coding standards.

This module provides consolidated command operations that follow the ULTMOS
coding standards:
- Uses subprocess instead of os.system
- Includes proper type hints
- Has specific exception handling
- Input validation to prevent command injection
- Structured logging
"""

import subprocess
import shlex
import platform
from typing import List, Dict, Tuple, Union, Optional, Any
import re
import shutil

# Import the centralized logger
from .logger import default_logger as log


def validate_command(command: List[str]) -> bool:
    """Validate that a command is safe to execute.
    
    Args:
        command: Command as a list of strings
        
    Returns:
        True if command is safe to execute, False otherwise
    """
    if not command:
        log.error(f"Empty command provided")
        return False
        
    # Check for shell metacharacters in command arguments
    dangerous_patterns = [
        r'\s*[|;&$]',  # Shell pipe, command separator, background, variable
        r'\s*[<>]',    # Redirections
        r'\s*`.*`',    # Backtick command execution
        r'\s*\$\(',    # Command substitution
        r'\s*\(\s*',   # Subshell
        r'\s*\{\s*',   # Block execution
    ]
    
    for arg in command:
        if not isinstance(arg, str):
            log.error(f"Command argument must be a string: {arg}")
            return False
            
        for pattern in dangerous_patterns:
            if re.search(pattern, arg):
                log.error(f"Potentially unsafe command argument: {arg}")
                return False
                
    return True


def run_command(
    command: List[str], 
    check: bool = False,
    quiet: bool = False,
    timeout: Optional[int] = None
) -> subprocess.CompletedProcess:
    """Run a command and return the result.
    
    Args:
        command: Command as a list of strings
        check: Whether to raise an exception on non-zero exit code
        quiet: If True, don't log messages
        timeout: Optional timeout in seconds
        
    Returns:
        A CompletedProcess instance
        
    Raises:
        ValueError: If command is invalid or empty
        subprocess.SubprocessError: If the process fails and check=True
        subprocess.TimeoutExpired: If the timeout is reached
    """
    if not validate_command(command):
        raise ValueError(f"Invalid command: {command}")
    
    cmd_display = ' '.join(shlex.quote(arg) for arg in command)
    if not quiet:
        log.info(f"Running command: {cmd_display}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=check,
            timeout=timeout
        )
        
        if not quiet:
            if result.returncode == 0:
                log.debug(f"Command succeeded with return code 0")
                if result.stdout.strip():
                    log.debug(f"Command output: {result.stdout.strip()}")
            else:
                log.warning(f"Command failed with return code {result.returncode}")
                if result.stderr.strip():
                    log.warning(f"Command error output: {result.stderr.strip()}")
        
        return result
        
    except subprocess.SubprocessError as e:
        if isinstance(e, subprocess.TimeoutExpired):
            if not quiet:
                log.error(f"Command timed out after {timeout} seconds", e)
        else:
            if not quiet:
                log.error(f"Error executing command", e)
        raise
    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error executing command", e)
        raise


def run_command_with_output(
    command: List[str],
    quiet: bool = False,
    timeout: Optional[int] = None
) -> Tuple[bool, str, str]:
    """Run a command and return success status with output.
    
    Args:
        command: Command as a list of strings
        quiet: If True, don't log messages
        timeout: Optional timeout in seconds
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        if not validate_command(command):
            return (False, "", "Invalid command")
            
        cmd_display = ' '.join(shlex.quote(arg) for arg in command)
        if not quiet:
            log.info(f"Running command: {cmd_display}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout
        )
        
        if not quiet:
            if result.returncode == 0:
                log.debug(f"Command succeeded with return code 0")
            else:
                log.warning(f"Command failed with return code {result.returncode}")
                
        return (result.returncode == 0, result.stdout, result.stderr)
        
    except subprocess.TimeoutExpired as e:
        if not quiet:
            log.error(f"Command timed out after {timeout} seconds", e)
        return (False, "", f"Command timed out after {timeout} seconds")
        
    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error executing command", e)
        return (False, "", str(e))


def check_command_exists(command: str, quiet: bool = False) -> bool:
    """Check if a command exists in the system PATH.
    
    Args:
        command: Name of the command to check
        quiet: If True, don't log messages
        
    Returns:
        True if command exists, False otherwise
    """
    try:
        if platform.system() == "Windows":
            # On Windows, use where command
            check_cmd = ["where", command]
        else:
            # On Unix-like systems, use which command
            check_cmd = ["which", command]
            
        result = subprocess.run(
            check_cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        exists = result.returncode == 0
        
        if not quiet:
            if exists:
                log.debug(f"Command '{command}' found at: {result.stdout.strip()}")
            else:
                log.debug(f"Command '{command}' not found")
                
        return exists
        
    except Exception as e:
        if not quiet:
            log.error(f"Error checking if command exists", e)
        return False


def run_virsh_command(
    subcommand: List[str], 
    quiet: bool = False
) -> Tuple[bool, str, str]:
    """Run a virsh command safely.
    
    Args:
        subcommand: Virsh subcommand and arguments as a list of strings
        quiet: If True, don't log messages
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    # Check if virsh is available
    if not check_command_exists("virsh", quiet=True):
        if not quiet:
            log.error("virsh command not found in PATH")
        return (False, "", "virsh command not found")
    
    # Create the full command
    command = ["virsh"] + subcommand
    
    # Run the command
    return run_command_with_output(command, quiet=quiet)


def run_sudo_command(
    command: List[str], 
    prompt: str = "This operation requires elevated privileges",
    quiet: bool = False
) -> Tuple[bool, str, str]:
    """Run a command with sudo.
    
    Args:
        command: Command and arguments as a list of strings
        prompt: Message to display when requesting sudo access
        quiet: If True, don't log messages
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    # Validate the command
    if not validate_command(command):
        if not quiet:
            log.error(f"Invalid sudo command")
        return (False, "", "Invalid command")
    
    # Show the prompt
    if not quiet:
        log.warning(f"{prompt} - executing with sudo: {' '.join(shlex.quote(arg) for arg in command)}")
    
    # Create the sudo command
    sudo_command = ["sudo"] + command
    
    # Run the command
    return run_command_with_output(sudo_command, quiet=quiet)


def clear_terminal(quiet: bool = False) -> None:
    """Clear the terminal screen in a platform-independent way.
    
    Args:
        quiet: If True, don't log messages
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            subprocess.run(["cls"], shell=True, check=False)
        else:
            subprocess.run(["clear"], check=False)
            
    except Exception as e:
        if not quiet:
            log.error(f"Error clearing terminal screen", e)


def get_terminal_size() -> Tuple[int, int]:
    """Get the terminal size in a platform-independent way.
    
    Returns:
        Tuple of (columns, rows) as integers
    """
    try:
        columns, rows = shutil.get_terminal_size()
        return columns, rows
    except Exception as e:
        log.debug(f"Error getting terminal size: {e}")
        return 80, 24  # Default size


def get_user_home(quiet: bool = False) -> str:
    """Get the actual user's home directory, even when running with sudo.
    
    Args:
        quiet: If True, don't log messages
        
    Returns:
        User home directory path
    """
    try:
        # Check if running as sudo
        sudo_user = None
        try:
            sudo_user_result = run_command_with_output(
                ["printenv", "SUDO_USER"], 
                quiet=True
            )
            
            if sudo_user_result[0]:  # Success
                sudo_user = sudo_user_result[1].strip()
        except Exception:
            pass
        
        if sudo_user:
            # Get the real user's home directory
            getent_result = run_command_with_output(
                ["getent", "passwd", sudo_user],
                quiet=True
            )
            
            if getent_result[0]:
                real_home = getent_result[1].strip().split(':')[5]
                if not quiet:
                    log.debug(f"Found home directory for sudo user {sudo_user}: {real_home}")
                return real_home
            
        # Fallback to current HOME
        home_result = run_command_with_output(
            ["printenv", "HOME"],
            quiet=True
        )
        
        if home_result[0]:
            home = home_result[1].strip()
            if not quiet:
                log.debug(f"Using current HOME: {home}")
            return home
            
        # Last resort fallback
        if not quiet:
            log.warning("Could not determine home directory, using current directory")
        return "."
        
    except Exception as e:
        if not quiet:
            log.error(f"Error determining user home directory", e)
        return "."
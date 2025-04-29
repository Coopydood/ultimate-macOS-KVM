#!/usr/bin/env python3

"""
Safe utility functions for disk operations used by the UMK cleanup tools.

This module follows the ULTMOS coding standards:
- Uses pathlib instead of os module
- Uses subprocess for command execution
- Includes type hints
- Has proper exception handling
- Includes safeguards against deleting physical disks
"""

import shutil
import time
from pathlib import Path
from typing import List, Dict, Optional, Set, Union, Tuple, Iterator

# Import safe utilities and logger
from .logger import default_logger as log
from .safe_command_utils import get_user_home
from .safe_file_utils import (
    is_valid_file,
    is_valid_directory,
    ensure_directory_exists,
    copy_file,
    move_file,
    delete_file as safe_delete_file # Avoid potential conflict if DiskImage has delete method
)
from .config_utils import BlobData # Keep config_utils for BlobData


class DiskImage:
    """Class representing a disk image file."""
    
    def __init__(self, path: Union[str, Path], is_physical: bool = False):
        """Initialize a disk image object.
        
        Args:
            path: Path to the disk image
            is_physical: Whether this is a physical disk
        """
        self.path = Path(path)
        self.is_physical = is_physical
        self._size: Optional[int] = None
        
    @property
    def size(self) -> int:
        """Get the size of the disk image.
        
        Returns:
            Size in bytes
        """
        if self._size is None:
            try:
                # Use safe util to check validity first
                if is_valid_file(self.path, quiet=True):
                    # Only call stat if it's a valid file
                    self._size = self.path.stat().st_size
                else:
                    # is_valid_file might log a warning if not quiet
                    self._size = 0
            except PermissionError as e:
                # Log specific permission error during stat
                log.warning(f"Permission denied getting size for {self.path}: {e}")
                self._size = 0
            except Exception as e:
                # Log unexpected errors during stat
                log.exception(f"Unexpected error getting size for {self.path}", e)
                self._size = 0
        # Ensure we return 0 if size couldn't be determined or is 0
        return self._size or 0

    @property
    def name(self) -> str:
        """Get the name of the disk image.
        
        Returns:
            Filename
        """
        return self.path.name
        
    @property
    def size_human(self) -> str:
        """Get human-readable size.
        
        Returns:
            Human-readable size string
        """
        size_bytes = self.size
        
        # Convert to appropriate unit
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size_unit = 0
        
        while size_bytes >= 1024 and size_unit < len(units) - 1:
            size_bytes /= 1024
            size_unit += 1
            
        return f"{size_bytes:.2f} {units[size_unit]}"
        
    def __str__(self) -> str:
        """String representation of the disk image."""
        physical_flag = " (PHYSICAL DEVICE)" if self.is_physical else ""
        return f"{self.path}{physical_flag} - {self.size_human}"


def find_disk_images(base_dir: Union[str, Path], patterns: List[str]) -> List[DiskImage]:
    """Find disk images in the base directory matching patterns.
    
    Args:
        base_dir: Base directory to search in
        patterns: List of glob patterns to match
        
    Returns:
        List of DiskImage objects
    """
    base_path = Path(base_dir)
    # Use safe util to check directory validity, log warning if invalid
    if not is_valid_directory(base_path, quiet=False):
        return []

    disk_images: Set[Path] = set()
    log.debug(f"Searching for disk images in {base_path} with patterns: {patterns}")

    for pattern in patterns:
        try:
            # Assuming patterns are relative to base_dir for simplicity and safety
            if Path(pattern).is_absolute():
                log.warning(f"Absolute pattern '{pattern}' ignored in find_disk_images. Use relative patterns.")
                continue

            # Use rglob for recursive search within base_dir
            for file_path in base_path.rglob(pattern):
                # Ensure it's a file using safe util (quiet internal check)
                if is_valid_file(file_path, quiet=True):
                    disk_images.add(file_path)
        except PermissionError as e:
             log.warning(f"Permission denied processing pattern '{pattern}': {e}")
        except Exception as e:
            # Log other unexpected errors during globbing
            log.exception(f"Error processing pattern '{pattern}' in find_disk_images", e)

    log.debug(f"Found {len(disk_images)} potential disk image paths.")
    # Create DiskImage objects (default to non-physical)
    return [DiskImage(path) for path in sorted(list(disk_images))]


def find_qcow2_images(base_dir: Union[str, Path]) -> List[DiskImage]:
    """Find QCOW2 disk images in the directory.
    
    Args:
        base_dir: Base directory to search in
        
    Returns:
        List of DiskImage objects
    """
    return find_disk_images(base_dir, ["**/*.qcow2"])


def find_raw_images(base_dir: Union[str, Path]) -> List[DiskImage]:
    """Find raw disk images in the directory.
    
    Args:
        base_dir: Base directory to search in
        
    Returns:
        List of DiskImage objects
    """
    return find_disk_images(base_dir, ["**/*.img", "**/*.raw"])


def get_disk_from_blob_data(blob_data: BlobData) -> Optional[DiskImage]:
    """Get disk image info from blob data.
    
    Args:
        blob_data: BlobData containing VM configuration
        
    Returns:
        DiskImage object if found, None otherwise
    """
    if not blob_data.disk_path:
        return None
        
    disk_path = blob_data.disk_path
    
    # Ensure the path exists and is a file using safe util, log warning if invalid
    if not is_valid_file(disk_path, quiet=False):
        return None

    return DiskImage(disk_path, is_physical=blob_data.is_physical_disk)


def check_disk_space(path: Union[str, Path], required_space: int) -> bool:
    """Check if there's enough disk space available.
    
    Args:
        path: Path to check space on
        required_space: Required space in bytes
        
    Returns:
        True if enough space available, False otherwise
    """
    try:
        # Convert to Path
        path_obj = Path(path)

        # Find the nearest existing parent directory to check space
        check_path = path_obj
        # Use safe util to check existence and type (quiet internal check)
        while not is_valid_directory(check_path, quiet=True):
            if check_path == check_path.parent: # Reached root or invalid path
                 log.error(f"Could not find existing directory to check disk space for path: {path}")
                 return False
            check_path = check_path.parent
            # Safeguard for root directory
            if str(check_path) == check_path.root: break


        # Get free space using shutil.disk_usage
        free_space = shutil.disk_usage(check_path).free
        has_enough_space = free_space >= required_space

        log.debug(f"Disk space check for {path}: Required={required_space}, Available on {check_path}={free_space}. Enough space: {has_enough_space}")
        return has_enough_space

    except FileNotFoundError as e:
        # This might occur if shutil.disk_usage fails on the path
        log.error(f"Path not found by shutil.disk_usage while checking disk space for: {path}: {e}")
        return False
    except PermissionError as e:
        log.error(f"Permission denied checking disk space for: {path}", e)
        return False
    except Exception as e:
        # Catch other potential errors from shutil.disk_usage
        log.exception(f"Unexpected error checking disk space for: {path}", e)
        return False


def backup_disk_image(
    disk_img: DiskImage, 
    backup_dir: Union[str, Path],
    quiet: bool = False
) -> Optional[Path]:
    """Backup a disk image if it's not a physical disk.
    
    Args:
        disk_img: DiskImage to backup
        backup_dir: Directory to store backup
        quiet: If True, suppress output messages
        
    Returns:
        Path to backup file if successful, None otherwise
    """
    # Never attempt to backup physical disks
    if disk_img.is_physical:
        if not quiet:
            log.warning(f"SAFETY: Will not backup physical disk {disk_img.path}")
        return None

    # Convert to Path
    backup_path = Path(backup_dir)
    
    # Ensure backup directory exists
    # Ensure backup directory exists using safe util
    if not ensure_directory_exists(backup_path, quiet=quiet):
        # ensure_directory_exists logs the error
        return None

    # Check if source exists and is a file using safe util
    if not is_valid_file(disk_img.path, quiet=quiet):
        # is_valid_file logs the warning/error
        return None

    # Check if we have enough space
    try:
        if not check_disk_space(backup_path, disk_img.size):
            if not quiet:
                log.error(f"Not enough space to backup {disk_img.path} (needs {disk_img.size_human})")
            return None
    except Exception as e:
         if not quiet:
              log.error(f"Failed to check disk space for backup", e)
         return None

    # Create backup filename with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_file = backup_path / f"{disk_img.name}.{timestamp}.bak"
    
    if not quiet:
        log.info(f"Backing up {disk_img.path} to {backup_file}")

    # Copy the file using safe util
    if copy_file(disk_img.path, backup_file, quiet=quiet):
        # copy_file logs success/failure
        return backup_file
    else:
        return None


def delete_disk_image(disk_img: DiskImage, quiet: bool = False) -> bool:
    """Delete a disk image if it's not a physical disk.

    Args:
        disk_img: DiskImage to delete
        quiet: If True, suppress output messages

    Returns:
        True if deleted successfully, False otherwise
    """
    if disk_img.is_physical:
        if not quiet:
            log.warning(f"SAFETY: Will not delete physical disk {disk_img.path}")
        return False

    # Delete using safe util (handles existence check and logging)
    # Pass quiet flag correctly
    return safe_delete_file(disk_img.path, quiet=quiet)


def move_disk_image(
    disk_img: DiskImage, 
    destination: Union[str, Path],
    quiet: bool = False
) -> bool:
    """Move a disk image if it's not a physical disk.
    
    Args:
        disk_img: DiskImage to move
        destination: Destination directory or file
        quiet: If True, suppress output messages
        
    Returns:
        True if moved successfully, False otherwise
    """
    # Never attempt to move physical disks
    if disk_img.is_physical:
        if not quiet:
            log.warning(f"SAFETY: Will not move physical disk {disk_img.path}")
        return False

    # Convert to Path
    dest_path = Path(destination)

    # Determine the final destination file path
    # Use quiet=True for internal check
    if is_valid_directory(dest_path, quiet=True):
        dest_file_path = dest_path / disk_img.name
    else:
        # Assume it's a full file path, ensure parent exists
        dest_file_path = dest_path
        # Use quiet=False here to log error if parent creation fails
        if not ensure_directory_exists(dest_file_path.parent, quiet=quiet):
             return False

    # Check if we have enough space on the destination's parent directory
    try:
        # Use quiet=False to log error if check fails
        if not check_disk_space(dest_file_path.parent, disk_img.size):
            if not quiet: # check_disk_space already logs errors
                 pass # Error logged by check_disk_space
            return False
    except Exception as e:
         # check_disk_space should handle its exceptions, but catch just in case
         if not quiet:
              log.exception(f"Unexpected error checking disk space for move", e)
         return False

    # Move the file using safe util, pass quiet flag
    return move_file(disk_img.path, dest_file_path, quiet=quiet)


def get_default_backup_dir() -> Path:
    """Get the default backup directory.
    
    Returns:
        Path to the default backup directory
    """
    # Get user's home directory using safe util
    home_dir_str = get_user_home(quiet=True) # Use quiet for internal call
    home_dir = Path(home_dir_str)

    # Create a timestamped directory in user's home
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    return home_dir / f"ultmos-backups-{timestamp}"
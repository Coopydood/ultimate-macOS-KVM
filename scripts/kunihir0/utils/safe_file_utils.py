#!/usr/bin/env python3

"""
Safe file operation utilities for kunihir0 that follow coding standards.

This module provides consolidated file operations that follow the ULTMOS
coding standards:
- Uses pathlib instead of os module
- Includes proper type hints
- Has specific exception handling
- Structured logging
- Avoids duplication and redundancy
"""

from pathlib import Path
import shutil
from typing import List, Union, Optional, Set, Iterator, Callable
import tempfile
import stat # For chmod constants
import time # For timestamp in backup dir
# Removed unused imports: subprocess, argparse, pwd, os

# Import the centralized logger
from .logger import default_logger as log


def is_valid_file(path: Union[str, Path], quiet: bool = False) -> bool:
    """Check if path exists and is a valid file.

    Args:
        path: Path to check
        quiet: If True, don't log warnings

    Returns:
        True if path exists and is a file
    """
    try:
        path_obj = Path(path)
        result = path_obj.exists() and path_obj.is_file()

        if not result and not quiet:
            log.warning(f"Path is not a valid file: {path}")

        return result
    except Exception as e:
        log.error(f"Error checking if path is a valid file", e)
        return False


def is_valid_directory(path: Union[str, Path], quiet: bool = False) -> bool:
    """Check if path exists and is a valid directory.

    Args:
        path: Path to check
        quiet: If True, don't log warnings

    Returns:
        True if path exists and is a directory
    """
    try:
        path_obj = Path(path)
        result = path_obj.exists() and path_obj.is_dir()

        if not result and not quiet:
            log.warning(f"Path is not a valid directory: {path}")

        return result
    except Exception as e:
        log.error(f"Error checking if path is a valid directory", e)
        return False


def delete_file(path: Union[str, Path], quiet: bool = False) -> bool:
    """Delete a file safely.

    Args:
        path: Path to the file to delete
        quiet: If True, don't log messages

    Returns:
        True if file was deleted successfully, False otherwise

    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If you don't have permission to delete the file
        IsADirectoryError: If the path is a directory, not a file
    """
    try:
        # Convert to Path object
        file_path = Path(path)

        # Check if it exists and is a file
        if not file_path.exists():
            if not quiet:
                log.warning(f"File doesn't exist: {file_path}")
            return False

        if not file_path.is_file():
            if not quiet:
                log.warning(f"Path is not a file: {file_path}")
            return False

        # Delete the file
        file_path.unlink()

        if not quiet:
            log.success(f"Deleted file: {file_path}")

        return True

    except FileNotFoundError as e:
        if not quiet:
            log.error(f"File not found", e)
        return False

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied when deleting file", e)
        return False

    except IsADirectoryError as e:
        if not quiet:
            log.error(f"Path is a directory, not a file", e)
        return False

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error deleting file", e)
        return False


def ensure_directory_exists(directory: Union[str, Path], quiet: bool = False) -> bool:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path to ensure exists
        quiet: If True, don't log messages

    Returns:
        True if directory exists or was created, False on error

    Raises:
        PermissionError: If you don't have permission to create the directory
        FileExistsError: If a file exists at the path
    """
    try:
        # Convert to Path object
        dir_path = Path(directory)

        # Create directory and parents if they don't exist
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            if not quiet:
                log.success(f"Created directory: {dir_path}")
        elif not dir_path.is_dir():
            if not quiet:
                log.error(f"Path exists but is not a directory: {dir_path}")
            return False

        return True

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied when creating directory", e)
        return False

    except FileExistsError as e:
        if not quiet:
            log.error(f"A file already exists at this path", e)
        return False

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error creating directory", e)
        return False


def delete_directory_tree(directory: Union[str, Path], quiet: bool = False) -> int:
    """Delete a directory and all its contents.

    Args:
        directory: Directory to delete
        quiet: If True, don't log messages

    Returns:
        Number of files deleted (approximate, based on initial count)

    Raises:
        FileNotFoundError: If the directory doesn't exist
        PermissionError: If you don't have permission
        NotADirectoryError: If the path is not a directory
    """
    try:
        # Convert to Path object
        dir_path = Path(directory)

        # Check if it exists and is a directory
        if not dir_path.exists():
            if not quiet:
                log.warning(f"Directory doesn't exist: {dir_path}")
            return 0

        if not dir_path.is_dir():
            if not quiet:
                log.warning(f"Path is not a directory: {dir_path}")
            return 0

        # Count files before deletion (approximate)
        file_count = 0
        try:
            file_count = sum(1 for item in dir_path.rglob('*') if item.is_file())
        except (PermissionError, OSError) as count_err:
            log.warning(f"Could not count all files in directory: {count_err}")
            # Continue with what we know is a partial count

        # Remove the directory and all its contents
        shutil.rmtree(dir_path, ignore_errors=True) # Ignore errors during removal

        # Check if it's gone after trying removal
        if not dir_path.exists():
            if not quiet:
                log.success(f"Removed directory tree: {dir_path} (approx {file_count} files)")
            return file_count
        else:
            if not quiet:
                 log.error(f"Failed to completely remove directory tree: {dir_path}. Some items may remain.")
            return 0 # Indicate failure if dir still exists

    except FileNotFoundError as e: # Should be caught by initial exists check, but belt-and-suspenders
        if not quiet:
            log.error(f"Directory not found during deletion attempt", e)
        return 0

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied when deleting directory", e)
        return 0

    except NotADirectoryError as e:
        if not quiet:
            log.error(f"Path is not a directory", e)
        return 0

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error deleting directory", e)
        return 0


def copy_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    quiet: bool = False
) -> bool:
    """Copy a file from source to destination.

    Args:
        source: Source file path
        destination: Destination file path
        quiet: If True, don't log messages

    Returns:
        True if file was copied successfully, False otherwise

    Raises:
        FileNotFoundError: If source doesn't exist
        PermissionError: If you don't have permission
        IsADirectoryError: If source is a directory
    """
    try:
        # Convert to Path objects
        src_path = Path(source)
        dest_path = Path(destination)

        # Check if source exists and is a file
        if not src_path.exists():
            if not quiet:
                log.warning(f"Source file doesn't exist: {src_path}")
            return False

        if not src_path.is_file():
            if not quiet:
                log.warning(f"Source path is not a file: {src_path}")
            return False

        # Create destination directory if it doesn't exist
        ensure_directory_exists(dest_path.parent, quiet=quiet)

        # Copy the file
        shutil.copy2(src_path, dest_path)

        if not quiet:
            log.success(f"Copied file: {src_path} → {dest_path}")
        return True

    except FileNotFoundError as e:
        if not quiet:
            log.error(f"Source file not found", e)
        return False

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied during copy operation", e)
        return False

    except IsADirectoryError as e:
        if not quiet:
            log.error(f"Source or destination is a directory", e)
        return False

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error copying file", e)
        return False


def move_file(
    source: Union[str, Path],
    destination: Union[str, Path],
    quiet: bool = False
) -> bool:
    """Move a file from source to destination.

    Args:
        source: Source file path
        destination: Destination file path
        quiet: If True, don't log messages

    Returns:
        True if file was moved successfully, False otherwise

    Raises:
        FileNotFoundError: If source doesn't exist
        PermissionError: If you don't have permission
        IsADirectoryError: If source is a directory
    """
    try:
        # Convert to Path objects
        src_path = Path(source)
        dest_path = Path(destination)

        # Check if source exists and is a file
        if not src_path.exists():
            if not quiet:
                log.warning(f"Source file doesn't exist: {src_path}")
            return False

        if not src_path.is_file():
            if not quiet:
                log.warning(f"Source path is not a file: {src_path}")
            return False

        # Create destination directory if it doesn't exist
        ensure_directory_exists(dest_path.parent, quiet=quiet)

        # Move the file
        shutil.move(str(src_path), str(dest_path))

        if not quiet:
            log.success(f"Moved file: {src_path} → {dest_path}")
        return True

    except FileNotFoundError as e:
        if not quiet:
            log.error(f"Source file not found", e)
        return False

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied during move operation", e)
        return False

    except IsADirectoryError as e:
        if not quiet:
            log.error(f"Source or destination is a directory", e)
        return False

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error moving file", e)
        return False


def find_files(
    base_dir: Union[str, Path],
    patterns: List[str],
    quiet: bool = False
) -> List[Path]:
    """Find files matching multiple patterns.

    Args:
        base_dir: Base directory to search in
        patterns: List of glob patterns to match
        quiet: If True, don't log messages

    Returns:
        List of matching file paths
    """
    try:
        # Convert to Path object
        base_path = Path(base_dir)

        if not base_path.exists() or not base_path.is_dir():
            if not quiet:
                log.warning(f"Base directory doesn't exist or is not a directory: {base_path}")
            return []

        matching_files: Set[Path] = set()

        for pattern in patterns:
            try:
                # Use rglob for recursive matching within base_dir
                for file_path in base_path.rglob(pattern):
                    if file_path.is_file(): # Ensure it's a file
                        matching_files.add(file_path)
            except Exception as e:
                if not quiet:
                    log.warning(f"Error processing pattern '{pattern}': {e}")

        return sorted(list(matching_files)) # Return sorted list

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error finding files", e)
        return []


def read_file_text(path: Union[str, Path], quiet: bool = False) -> Optional[str]:
    """Read text content from a file.

    Args:
        path: Path to the file to read
        quiet: If True, don't log messages

    Returns:
        File contents as string, or None on error
    """
    try:
        file_path = Path(path)

        if not file_path.exists():
            if not quiet:
                log.warning(f"File doesn't exist: {file_path}")
            return None

        if not file_path.is_file():
            if not quiet:
                log.warning(f"Path is not a file: {file_path}")
            return None

        content = file_path.read_text(encoding='utf-8', errors='ignore') # Specify encoding

        if not quiet:
            log.debug(f"Read {len(content)} characters from {file_path}")

        return content

    except FileNotFoundError as e:
        if not quiet:
            log.error(f"File not found", e)
        return None

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied when reading file", e)
        return None

    except IsADirectoryError as e:
        if not quiet:
            log.error(f"Path is a directory, not a file", e)
        return None

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error reading file", e)
        return None


def write_file_text(
    path: Union[str, Path],
    content: str,
    quiet: bool = False
) -> bool:
    """Write text content to a file.

    Args:
        path: Path to the file to write
        content: Text content to write
        quiet: If True, don't log messages

    Returns:
        True if file was written successfully, False otherwise
    """
    try:
        file_path = Path(path)

        # Create parent directory if it doesn't exist
        ensure_directory_exists(file_path.parent, quiet=quiet)

        # Write the file
        file_path.write_text(content, encoding='utf-8') # Specify encoding

        if not quiet:
            log.success(f"Wrote {len(content)} characters to {file_path}")

        return True

    except PermissionError as e:
        if not quiet:
            log.error(f"Permission denied when writing file", e)
        return False

    except IsADirectoryError as e:
        if not quiet:
            log.error(f"Path is a directory, not a file", e)
        return False

    except Exception as e:
        if not quiet:
            log.exception(f"Unexpected error writing file", e)
        return False


# --- Self-Destruct Script Creation (Python Version - Copy Method) ---

def create_self_destruct_script(
    directory_to_delete: Union[str, Path],
    keep_disks: bool, # Argument still needed for passing to the script
    vm_names: List[str], # Argument still needed for passing to the script
    quiet: bool = False
) -> Optional[str]:
    """Copies the self_destruct_logic.py script to a temporary location
    and makes it executable.

    Args:
        directory_to_delete: The absolute path to the project directory to remove
                             (passed as arg to the copied script).
        keep_disks: If True, the copied script will attempt backups.
                    If False, it will attempt --remove-all-storage.
                    (Passed as arg to the copied script).
        vm_names: A list of VM names to attempt undefining.
                  (Passed as arg to the copied script).
        quiet: If True, suppress log messages from this function.

    Returns:
        The absolute path to the temporary Python script, or None on failure.
    """
    try:
        target_dir_path = Path(directory_to_delete).resolve() # Ensure absolute path
        if not quiet:
            log.info(f"Preparing self-destruct script for directory: {target_dir_path}")

        # --- Find the source script ---
        # Assumes this script (safe_file_utils.py) is in scripts/kunihir0/utils
        source_script_path = Path(__file__).parent / "self_destruct_logic.py"
        if not source_script_path.is_file():
            log.error(f"Source self-destruct script not found at: {source_script_path}")
            return None

        # --- Create temporary destination ---
        # Create a temp file with pathlib approach
        temp_dir = Path(tempfile.gettempdir())
        temp_script_path = temp_dir / f"ultmos_cleanup_{int(time.time())}.py"

        # --- Copy the script ---
        shutil.copy2(source_script_path, temp_script_path)

        # --- Make executable ---
        # Make executable by owner, readable by others
        temp_script_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IROTH)

        if not quiet:
            log.success(f"Copied self-destruct script to temporary location: {temp_script_path}")
        return str(temp_script_path)

    except (FileNotFoundError, PermissionError) as e:
        log.exception("Failed to find or access self-destruct script", e)
        return None
    except shutil.Error as e:
        log.exception("Failed to copy self-destruct script", e)
        return None
    except ValueError as e:
        log.exception("Invalid path or argument", e)
        return None
    except Exception as e:
        log.exception("Unexpected error creating/copying self-destruct script", e)
        # Clean up temp file if created
        try:
            if 'temp_script_path' in locals() and temp_script_path.exists():
                temp_script_path.unlink(missing_ok=True)
        except (FileNotFoundError, PermissionError, IsADirectoryError) as cleanup_err:
            log.error(f"Error during cleanup: {cleanup_err}")
        return None

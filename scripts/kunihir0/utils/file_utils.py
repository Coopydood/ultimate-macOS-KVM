#!/usr/bin/env python3

"""
Utility functions for file operations used by the UMK cleanup tools.
"""

import os
import glob
import shutil
from typing import List, Tuple

def delete_file(path: str, quiet: bool = False) -> bool:
    """Delete a file and print the result

    Args:
        path: Path to the file to delete
        quiet: If True, don't print deletion messages

    Returns:
        bool: True if file was deleted, False otherwise
    """
    try:
        if os.path.exists(path):
            os.remove(path)
            if not quiet:
                print(f"✓ Removed: {path}")
            return True
        return False
    except Exception as e:
        if not quiet:
            print(f"✗ Failed to remove {path}: {str(e)}")
        return False

def delete_files_in_directory(directory: str, pattern: str = "*", quiet: bool = False) -> int:
    """Delete all files matching the pattern in a directory

    Args:
        directory: Directory to clean
        pattern: Glob pattern to match files
        quiet: If True, don't print deletion messages

    Returns:
        int: Number of files deleted
    """
    try:
        if not os.path.exists(directory):
            return 0
        
        count = 0
        for file_path in glob.glob(os.path.join(directory, pattern)):
            if os.path.isfile(file_path):
                if delete_file(file_path, quiet):
                    count += 1
        return count
    except Exception as e:
        if not quiet:
            print(f"Error cleaning directory {directory}: {str(e)}")
        return 0

def delete_directory_tree(directory: str, quiet: bool = False) -> int:
    """Delete a directory and all its contents

    Args:
        directory: Directory to delete
        quiet: If True, don't print deletion messages

    Returns:
        int: Number of files and directories deleted
    """
    try:
        if not os.path.exists(directory):
            return 0
            
        # Count files before deletion
        file_count = 0
        for _, _, files in os.walk(directory):
            file_count += len(files)
            
        # Remove the directory and all its contents
        shutil.rmtree(directory)
        if not quiet:
            print(f"✓ Removed directory tree: {directory}")
        
        return file_count
    except Exception as e:
        if not quiet:
            print(f"✗ Failed to remove directory {directory}: {str(e)}")
        return 0

def find_files(base_dir: str, patterns: List[str]) -> List[str]:
    """Find files matching multiple patterns

    Args:
        base_dir: Base directory to search in
        patterns: List of glob patterns

    Returns:
        List[str]: List of matching file paths
    """
    matching_files = []
    for pattern in patterns:
        # Handle absolute patterns or relative patterns
        if os.path.isabs(pattern):
            pattern_path = pattern
        else:
            pattern_path = os.path.join(base_dir, pattern)
            
        for file_path in glob.glob(pattern_path, recursive=True):
            if os.path.isfile(file_path):
                matching_files.append(file_path)
    
    return matching_files

def delete_file_list(file_list: List[str], quiet: bool = False) -> int:
    """Delete a list of specific files

    Args:
        file_list: List of file paths to delete
        quiet: If True, don't print deletion messages

    Returns:
        int: Number of files deleted
    """
    count = 0
    for file_path in file_list:
        if delete_file(file_path, quiet):
            count += 1
    return count

def ensure_directory_exists(directory: str) -> bool:
    """Ensure a directory exists, creating it if necessary

    Args:
        directory: Directory path to check/create

    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False
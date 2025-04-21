#!/usr/bin/env python3

"""
UMK Temporary File Cleanup Utility

This script cleans up all temporary and generated files created during the VM setup process.
It uses modular design to make maintenance and extension easier.
"""

import os
import sys
import glob
import shutil
import argparse
from typing import Dict, List, Optional, Tuple, Union

# Import our utility modules
try:
    from file_utils import (
        delete_file, 
        delete_files_in_directory,
        delete_directory_tree,
        find_files,
        delete_file_list
    )
    from clean_config import CLEANER_GROUPS, ALL_PATTERNS
except ImportError:
    # When imported from another directory, adjust the path
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    try:
        from file_utils import (
            delete_file, 
            delete_files_in_directory,
            delete_directory_tree,
            find_files,
            delete_file_list
        )
        from clean_config import CLEANER_GROUPS, ALL_PATTERNS
    except ImportError:
        print("Error: Required utility modules not found.")
        sys.exit(1)


# ANSI colors for better output
class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class UMKCleaner:
    """Main cleaner class with modular cleaning capabilities"""
    
    def __init__(self, base_dir: str = ".", quiet: bool = False, dry_run: bool = False):
        """Initialize the cleaner
        
        Args:
            base_dir: Base directory for cleaning operations
            quiet: If True, reduce output verbosity
            dry_run: If True, only show what would be deleted without actually deleting
        """
        self.base_dir = os.path.abspath(base_dir)
        self.quiet = quiet
        self.dry_run = dry_run
        self.total_removed = 0
        self.cleaner_registry = {}
        self._register_cleaners()
        
    def _register_cleaners(self):
        """Register all cleaner functions"""
        self.cleaner_registry = {
            "logs": self.clean_logs,
            "main": self.clean_main_directory, 
            "blobs": self.clean_blobs_directory,
            "resources": self.clean_resources,
            "boot": self.clean_boot_files,
            "ovmf": self.clean_ovmf_files,
            "pycache": self.clean_pycache,
            "script_store": self.clean_script_store
        }
        
    def log(self, message: str, color: str = "", bold: bool = False):
        """Print a log message with optional formatting
        
        Args:
            message: The message to print
            color: ANSI color code to use
            bold: Whether to make the text bold
        """
        if self.quiet:
            return
            
        # Apply formatting
        formatted = message
        if bold:
            formatted = f"{Colors.BOLD}{formatted}"
        if color:
            formatted = f"{color}{formatted}"
        if bold or color:
            formatted = f"{formatted}{Colors.END}"
            
        print(formatted)
        
    def clean_logs(self) -> int:
        """Clean log files"""
        self.log("\nCleaning log files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["logs"]["patterns"]
        
        count = 0
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                count += delete_files_in_directory(os.path.join(self.base_dir, "logs"), 
                                                os.path.basename(pattern), 
                                                self.quiet)
                
        self.log(f"Removed {count} log files", Colors.GREEN)
        return count
        
    def clean_main_directory(self) -> int:
        """Clean files in the main directory"""
        self.log("\nCleaning root directory files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["main"]["patterns"]
        
        count = 0
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                if delete_file(os.path.join(self.base_dir, pattern), self.quiet):
                    count += 1
                    
        self.log(f"Removed {count} files from root directory", Colors.GREEN)
        return count
        
    def clean_blobs_directory(self) -> int:
        """Clean all APB blob files"""
        self.log("\nCleaning blob files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["blobs"]["patterns"]
        
        count = 0
        for pattern in patterns:
            directory = os.path.dirname(os.path.join(self.base_dir, pattern))
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                count += delete_files_in_directory(directory, 
                                                os.path.basename(pattern), 
                                                self.quiet)
                
        self.log(f"Removed {count} blob files", Colors.GREEN)
        return count
        
    def clean_resources(self) -> int:
        """Clean resource files"""
        self.log("\nCleaning resource files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["resources"]["patterns"]
        
        count = 0
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                if delete_file(os.path.join(self.base_dir, pattern), self.quiet):
                    count += 1
                    
        self.log(f"Removed {count} resource files", Colors.GREEN)
        return count
        
    def clean_boot_files(self) -> int:
        """Clean boot files"""
        self.log("\nCleaning boot files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["boot"]["patterns"]
        
        count = 0
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                if delete_file(os.path.join(self.base_dir, pattern), self.quiet):
                    count += 1
                    
        self.log(f"Removed {count} boot files", Colors.GREEN)
        return count
        
    def clean_ovmf_files(self) -> int:
        """Clean OVMF files"""
        self.log("\nCleaning OVMF files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["ovmf"]["patterns"]
        
        count = 0
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                if delete_file(os.path.join(self.base_dir, pattern), self.quiet):
                    count += 1
                    
        self.log(f"Removed {count} OVMF files", Colors.GREEN)
        return count
        
    def clean_pycache(self) -> int:
        """Clean Python bytecode files"""
        self.log("\nCleaning Python bytecode files...", Colors.BLUE, bold=True)
        
        count = 0
        # First try specific patterns
        patterns = CLEANER_GROUPS["pycache"]["patterns"]
        
        # Process specific patterns
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                directory = os.path.dirname(os.path.join(self.base_dir, pattern))
                count += delete_files_in_directory(directory, 
                                                os.path.basename(pattern), 
                                                self.quiet)
        
        # Also look for all __pycache__ directories
        if not self.dry_run:
            for root, dirs, _ in os.walk(self.base_dir):
                for dir_name in dirs:
                    if dir_name == "__pycache__":
                        pycache_dir = os.path.join(root, dir_name)
                        self.log(f"Cleaning directory: {pycache_dir}")
                        
                        # Remove all .pyc files
                        pyc_count = delete_files_in_directory(pycache_dir, "*.pyc", self.quiet)
                        count += pyc_count
                        
                        # Try to remove the directory if empty
                        try:
                            if not os.listdir(pycache_dir):
                                os.rmdir(pycache_dir)
                                self.log(f"✓ Removed empty directory: {pycache_dir}")
                        except Exception as e:
                            if not self.quiet:
                                self.log(f"✗ Failed to remove directory {pycache_dir}: {str(e)}", 
                                         Colors.RED)
        
        self.log(f"Removed {count} Python bytecode files in total", Colors.GREEN)
        return count
        
    def clean_script_store(self) -> int:
        """Clean script store files"""
        self.log("\nCleaning script store files...", Colors.BLUE, bold=True)
        patterns = CLEANER_GROUPS["script_store"]["patterns"]
        
        count = 0
        for pattern in patterns:
            if self.dry_run:
                matching_files = find_files(self.base_dir, [pattern])
                self.log(f"Would remove {len(matching_files)} files matching {pattern}")
                count += len(matching_files)
            else:
                directory = os.path.dirname(os.path.join(self.base_dir, pattern))
                count += delete_files_in_directory(directory, 
                                                os.path.basename(pattern), 
                                                self.quiet)
                    
        self.log(f"Removed {count} script store files", Colors.GREEN)
        return count
        
    def verify_cleanup(self) -> List[str]:
        """Verify all files have been cleaned
        
        Returns:
            List[str]: List of files that still exist and should be cleaned
        """
        self.log("\nVerifying all files have been cleaned...", Colors.BLUE, bold=True)
        
        # Find all files that should be cleaned
        remaining_files = []
        for pattern in ALL_PATTERNS:
            # Handle wildcard patterns
            if '*' in pattern:
                for file_path in glob.glob(os.path.join(self.base_dir, pattern)):
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        remaining_files.append(file_path)
            # Handle direct file paths
            else:
                file_path = os.path.join(self.base_dir, pattern)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    remaining_files.append(file_path)
                    
        return remaining_files
    
    def clean_remaining(self, remaining_files: List[str]) -> int:
        """Clean remaining files that weren't caught by the modular cleaners
        
        Args:
            remaining_files: List of files to clean
            
        Returns:
            int: Number of files cleaned
        """
        if not remaining_files:
            return 0
            
        self.log(f"\nFound {len(remaining_files)} files that still need cleaning:", 
                Colors.YELLOW)
        for file_path in remaining_files:
            self.log(f"  - {file_path}")
            
        self.log("\nCleaning remaining files...", Colors.BLUE)
        
        if self.dry_run:
            self.log(f"Would remove {len(remaining_files)} remaining files")
            return len(remaining_files)
            
        # Try to clean them directly
        cleaned = delete_file_list(remaining_files, self.quiet)
        self.log(f"Successfully removed an additional {cleaned} files", Colors.GREEN)
        return cleaned
        
    def clean_all(self) -> int:
        """Run all cleaners
        
        Returns:
            int: Total number of files cleaned
        """
        self.total_removed = 0
        
        # Run each registered cleaner
        for cleaner_id, cleaner_func in self.cleaner_registry.items():
            if cleaner_id in CLEANER_GROUPS:
                self.total_removed += cleaner_func()
                
        # Verify and clean remaining files
        if not self.dry_run:
            remaining_files = self.verify_cleanup()
            self.total_removed += self.clean_remaining(remaining_files)
            
        return self.total_removed
        
    def clean_selected(self, selected_cleaners: List[str]) -> int:
        """Run only selected cleaners
        
        Args:
            selected_cleaners: List of cleaner IDs to run
            
        Returns:
            int: Total number of files cleaned
        """
        self.total_removed = 0
        
        # Run only selected cleaners
        for cleaner_id in selected_cleaners:
            if cleaner_id in self.cleaner_registry:
                self.total_removed += self.cleaner_registry[cleaner_id]()
            else:
                self.log(f"Unknown cleaner: {cleaner_id}", Colors.RED)
                
        # Always verify and clean remaining files
        if not self.dry_run:
            remaining_files = self.verify_cleanup()
            self.total_removed += self.clean_remaining(remaining_files)
            
        return self.total_removed


def print_header():
    """Print script header"""
    print("\n" + "="*60)
    print(" UMK File Cleanup Utility ".center(60, "="))
    print("="*60)
    print("\nThis script will remove all temporary and generated files\n")


def confirm_action() -> bool:
    """Ask for confirmation before proceeding
    
    Returns:
        bool: True if user confirmed, False otherwise
    """
    response = input("Are you sure you want to proceed with cleanup? (y/N): ").lower()
    return response in ['y', 'yes']


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


def parse_arguments():
    """Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="UMK Temporary File Cleanup Utility"
    )
    
    # Basic options
    parser.add_argument("-y", "--yes", action="store_true", 
                      help="Skip confirmation prompt")
    parser.add_argument("-q", "--quiet", action="store_true", 
                      help="Reduce output verbosity")
    parser.add_argument("-n", "--dry-run", action="store_true", 
                      help="Show what would be deleted without actually deleting")
    
    # Selective cleaning options
    parser.add_argument("--logs", action="store_true", 
                      help="Clean log files only")
    parser.add_argument("--blobs", action="store_true", 
                      help="Clean blob files only")
    parser.add_argument("--root", action="store_true", 
                      help="Clean root directory files only")
    parser.add_argument("--resources", action="store_true", 
                      help="Clean resource files only")
    parser.add_argument("--boot", action="store_true", 
                      help="Clean boot files only")
    parser.add_argument("--ovmf", action="store_true", 
                      help="Clean OVMF files only")
    parser.add_argument("--pycache", action="store_true", 
                      help="Clean Python bytecode files only")
    parser.add_argument("--scripts", action="store_true", 
                      help="Clean script store files only")
    
    return parser.parse_args()


def clean_logs() -> int:
    """Clean log files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_logs()


def clean_main_directory() -> int:
    """Clean main directory files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_main_directory()


def clean_blobs_directory() -> int:
    """Clean blob files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_blobs_directory()


def clean_resources() -> int:
    """Clean resource files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_resources()


def clean_pycache() -> int:
    """Clean Python bytecode files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_pycache()


def clean_script_store() -> int:
    """Clean script store files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_script_store()


def clean_boot_files() -> int:
    """Clean boot files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_boot_files()


def clean_ovmf_files() -> int:
    """Clean OVMF files (exported function)"""
    cleaner = UMKCleaner(get_project_root())
    return cleaner.clean_ovmf_files()


def main():
    """Main function"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Show header unless quiet mode
    if not args.quiet:
        print_header()
    
    # Determine project root directory
    project_root = get_project_root()
    
    # Check if we're in the right directory
    if not os.path.exists(os.path.join(project_root, "main.py")):
        print(f"{Colors.RED}Error: Could not find UMK project root directory.{Colors.END}")
        print(f"{Colors.RED}This script must be run from within the UMK directory structure.{Colors.END}")
        return 1
    
    # Create cleaner instance
    cleaner = UMKCleaner(project_root, args.quiet, args.dry_run)
    
    # Determine which cleaners to run
    selected_cleaners = []
    if args.logs:
        selected_cleaners.append("logs")
    if args.blobs:
        selected_cleaners.append("blobs")
    if args.root:
        selected_cleaners.append("main")
    if args.resources:
        selected_cleaners.append("resources")
    if args.boot:
        selected_cleaners.append("boot")
    if args.ovmf:
        selected_cleaners.append("ovmf")
    if args.pycache:
        selected_cleaners.append("pycache")
    if args.scripts:
        selected_cleaners.append("script_store")
    
    # Print summary unless quiet mode
    if not args.quiet:
        if selected_cleaners:
            print(f"Running selected cleaners: {', '.join(selected_cleaners)}")
        else:
            print(f"Running all cleaners")
    
    # Ask for confirmation unless --yes flag
    if not args.yes and not args.dry_run:
        if not confirm_action():
            print("Cleanup cancelled.")
            return 0
    
    # Run cleaners
    if args.dry_run:
        print(f"{Colors.YELLOW}[DRY RUN] No files will actually be deleted{Colors.END}")
    
    # Run selected cleaners or all of them
    total_removed = 0
    if selected_cleaners:
        total_removed = cleaner.clean_selected(selected_cleaners)
    else:
        total_removed = cleaner.clean_all()
    
    # Print summary
    action = "Would remove" if args.dry_run else "Removed"
    print(f"\n{Colors.GREEN}Cleanup completed. {action} {total_removed} files in total.{Colors.END}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
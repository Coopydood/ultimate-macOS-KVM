#!/usr/bin/env python3

"""
Type-safe configuration utilities for the UMK cleanup tools.

This module provides typed configuration classes that enforce validation
and ensure predictable behavior for the uninstaller. It follows the ULTMOS
coding standards with type hints and proper validation.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

# Import the centralized logger
from .logger import default_logger as log
# Import safe file utils for reading/writing
from .safe_file_utils import read_file_text, write_file_text, ensure_directory_exists


@dataclass
class CleanupConfig:
    """Configuration for file cleanup operations."""
    
    # Base directory for operations
    base_dir: Path
    
    # Patterns of files to clean up 
    patterns: List[str] = field(default_factory=list)
    
    # Patterns of files to preserve (never delete)
    preserve_patterns: List[str] = field(default_factory=list)
    
    # Whether to suppress output messages
    quiet: bool = False
    
    def __post_init__(self) -> None:
        """Validate and normalize configuration."""
        # Convert string to Path if needed
        if isinstance(self.base_dir, str):
            self.base_dir = Path(self.base_dir)
            
        # Ensure patterns is a list
        if not isinstance(self.patterns, list):
            self.patterns = []
            
        # Ensure preserve_patterns is a list
        if not isinstance(self.preserve_patterns, list):
            self.preserve_patterns = []
    
    def should_preserve(self, filepath: Path) -> bool:
        """Check if a file should be preserved based on patterns.
        
        Args:
            filepath: Path to check against preserve patterns
            
        Returns:
            True if file should be preserved, False if it can be deleted
        """
        # Convert to Path if needed
        path = Path(filepath)
        
        # Check each preserve pattern
        for pattern in self.preserve_patterns:
            if path.match(pattern):
                return True
        
        return False


@dataclass
class UninstallConfig:
    """Configuration for the uninstaller."""
    
    # Whether to keep VM disk images
    keep_disks: bool = True
    
    # Where to backup files that are preserved
    backup_dir: Optional[Path] = None
    
    # Whether to clean temporary files
    clean_temp: bool = True
    
    # Whether to remove VMs from libvirt
    remove_vms: bool = True
    
    # Whether to show confirmation prompts
    confirm_actions: bool = True
    
    # Whether to run in dry run mode (no actual changes)
    dry_run: bool = False
    
    # Critical operation timeout in seconds 
    timeout: int = 5
    
    def __post_init__(self) -> None:
        """Validate and normalize configuration."""
        # Convert string to Path if needed
        if isinstance(self.backup_dir, str):
            self.backup_dir = Path(self.backup_dir)
            
        # Ensure timeout is reasonable
        if self.timeout < 0:
            self.timeout = 5


@dataclass
class BlobData:
    """Container for user VM configuration data from blobs."""
    
    # Boot script name
    boot_script: Optional[str] = None
    
    # VM name
    vm_name: Optional[str] = None
    
    # Virtual disk path
    disk_path: Optional[Path] = None
    
    # Whether disk is a physical device
    is_physical_disk: bool = False
    
    # Target OS version
    target_os: Optional[str] = None
    
    # Target OS name
    target_os_name: Optional[str] = None
    
    @classmethod
    def from_blob_dir(cls, blob_dir: Union[str, Path]) -> "BlobData":
        """Load blob data from the blobs directory.
        
        Args:
            blob_dir: Path to blobs directory
            
        Returns:
            BlobData object with populated fields
        """
        # Convert to Path if needed
        blob_path = Path(blob_dir)
        data = cls()
        
        # Try to read each blob file
        try:
            user_dir = blob_path / "user"
            
            # Boot script
            boot_script_path = user_dir / "USR_CFG.apb"
            if boot_script_path.exists():
                data.boot_script = boot_script_path.read_text().strip()
            
            # VM name
            vm_name_path = user_dir / "USR_VM_NAME.apb"
            if vm_name_path.exists():
                data.vm_name = vm_name_path.read_text().strip()
                
            # Disk path
            disk_path_blob = user_dir / "USR_HDD_PATH.apb"
            if disk_path_blob.exists():
                disk_path_text = disk_path_blob.read_text().strip()
                # Handle VM_PATH variable
                if "$VM_PATH" in disk_path_text:
                    # VM_PATH is the repo root
                    repo_root = blob_path.parent
                    disk_path_text = disk_path_text.replace("$VM_PATH", str(repo_root))
                data.disk_path = Path(disk_path_text)
                
            # Physical disk flag
            physical_path = user_dir / "USR_HDD_ISPHYSICAL.apb"
            if physical_path.exists():
                is_physical = physical_path.read_text().strip().lower()
                data.is_physical_disk = is_physical == "true"
                
            # OS version
            os_path = user_dir / "USR_TARGET_OS.apb"
            if os_path.exists():
                data.target_os = os_path.read_text().strip()
                
            # OS name
            os_name_path = user_dir / "USR_TARGET_OS_NAME.apb"
            if os_name_path.exists():
                data.target_os_name = os_name_path.read_text().strip()

        except FileNotFoundError as e:
            log.warning(f"Blob file not found during read: {e}")
        except PermissionError as e:
            log.error(f"Permission denied reading blob data", e)
        except IsADirectoryError as e:
            log.error(f"Expected blob file but found directory", e)
        except Exception as e:
            log.exception(f"Unexpected error reading blob data", e)

        return data


def load_config(config_file: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    Args:
        config_file: Path to JSON configuration file
        
    Returns:
        Dictionary of configuration values
    """
    # Convert to Path if needed
    config_path = Path(config_file)
    
    content = read_file_text(config_path, quiet=True) # Use quiet=True for internal check
    if content is None:
        log.warning(f"Config file not found or could not be read: {config_file}")
        return {}

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        log.error(f"Error decoding JSON from config file {config_file}", e)
        return {}
    except Exception as e:
        log.exception(f"Unexpected error loading config file {config_file}", e)
        return {}


def save_config(config_data: Dict[str, Any], config_file: Union[str, Path]) -> bool:
    """Save configuration to a JSON file.
    
    Args:
        config_data: Dictionary of configuration values
        config_file: Path to save JSON configuration
        
    Returns:
        True if saved successfully, False otherwise
    """
    # Convert to Path if needed
    config_path = Path(config_file)
    
    try:
        # Ensure parent directory exists using safe util
        if not ensure_directory_exists(config_path.parent, quiet=True):
             log.error(f"Could not create parent directory for config file {config_file}")
             return False

        # Serialize data to JSON string
        json_content = json.dumps(config_data, indent=2)

        # Write using safe util
        if write_file_text(config_path, json_content, quiet=True):
            log.debug(f"Saved configuration to {config_file}")
            return True
        else:
            # write_file_text already logs the error
            return False

    except TypeError as e:
        log.error(f"Data is not JSON serializable for config file {config_file}", e)
        return False
    except Exception as e:
        log.exception(f"Unexpected error saving config file {config_file}", e)
        return False


def get_critical_files() -> List[str]:
    """Get patterns for critical files that should never be deleted.
    
    Returns:
        List of file patterns that should be preserved
    """
    return [
        "boot/OpenCore.qcow2",
        "ovmf/OVMF_CODE.fd",
        "ovmf/OVMF_VARS.fd",
        "resources/script_store/*",
        "blobs/user/*"
    ]


def get_cleanup_tiers() -> Dict[str, Dict[str, Any]]:
    """Get defined cleanup tiers with increasing levels of deletion.
    
    Returns:
        Dictionary of cleanup tiers
    """
    # Define patterns for different types of files
    log_patterns = ["logs/APC_RUN_*.log"]
    temp_patterns = ["*.tmp", "*.log", "*.bak", "tmp/*"]
    blob_stale_patterns = ["blobs/stale/USR_*.apb"]
    blob_main_patterns = ["blobs/USR_*.apb"]
    resource_patterns = [
        "resources/BaseSystem.dmg",
        "resources/BaseSystem.img",
        "resources/.notices",
        "resources/config.sh"
    ]
    pycache_patterns = [
        "resources/python/__pycache__/*.pyc",
        "resources/python/pypresence/__pycache__/*.pyc"
    ]
    
    # Combine all patterns for the aggressive tier
    all_patterns = (
        log_patterns + temp_patterns + blob_stale_patterns +
        blob_main_patterns + resource_patterns + pycache_patterns
    )
    
    # Critical files that should never be deleted
    critical_files = get_critical_files()
    
    return {
        "safe": {
            "description": "Only cleanup temporary files, logs, and stale blobs",
            "patterns": (log_patterns + temp_patterns + 
                        blob_stale_patterns + pycache_patterns)
        },
        "moderate": {
            "description": "Also remove downloaded images and cached data",
            "patterns": (log_patterns + temp_patterns + 
                        blob_stale_patterns + blob_main_patterns +
                        resource_patterns + pycache_patterns)
        },
        "aggressive": {
            "description": "Remove everything except VM data and essentials",
            "patterns": all_patterns,
            "preserve": critical_files
        }
    }


def get_safe_patterns(include_critical: bool = False) -> List[str]:
    """Get file patterns that are safe to clean.
    
    Args:
        include_critical: Whether to include critical patterns
        
    Returns:
        List of safe patterns to clean
    """
    # Define non-critical patterns
    safe_patterns = [
        "*.tmp",
        "*.log",
        "*.bak",
        "tmp/*",
        "logs/APC_RUN_*.log",
        "blobs/stale/USR_*.apb",
        "resources/python/__pycache__/*.pyc"
    ]
    
    if include_critical:
        # Add potentially critical patterns
        safe_patterns.extend([
            "blobs/user/USR_*.apb",
            "boot/OpenCore.qcow2",
            "ovmf/OVMF_CODE.fd",
            "ovmf/OVMF_VARS.fd"
        ])
    
    return safe_patterns


def is_critical_file(pattern: str) -> bool:
    """Check if a file pattern is marked as critical.
    
    Args:
        pattern: File pattern to check
        
    Returns:
        True if pattern is critical, False otherwise
    """
    critical_patterns = get_critical_files()
    
    # Direct match
    if pattern in critical_patterns:
        return True
    
    # Check for matching paths/patterns
    for critical_pattern in critical_patterns:
        if "*" in critical_pattern:
            # Convert glob pattern to simple check
            pattern_base = critical_pattern.replace("*", "")
            if pattern_base in pattern:
                return True
                
    return False
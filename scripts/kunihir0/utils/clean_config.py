#!/usr/bin/env python3

"""
Safe configuration for the ULTMOS cleanup utility.

Defines patterns of files to clean in different categories with proper
typing and protection flags for critical files. This follows the ULTMOS
coding standards with type hints and safety measures.
"""

from typing import Dict, List, Set, Union, Any
from pathlib import Path


# Type definitions for pattern configurations
PatternList = List[str]
PatternDict = Dict[str, PatternList]
CleanerGroup = Dict[str, Union[str, PatternList]]
CleanerGroups = Dict[str, CleanerGroup]


# Log file patterns
LOG_PATTERNS: PatternList = [
    "logs/APC_RUN_*.log"
]

# Main directory file patterns
ROOT_PATTERNS: PatternList = [
    "BaseSystem.img",  # Installer image
    "boot.sh",         # Boot script
    "HDD.qcow2",       # Main disk image
    "boot.xml"         # Boot xml import
]

# Blob file patterns (in various directories)
BLOB_PATTERNS: PatternDict = {
    "main": [
        "blobs/USR_*.apb"  # Current session blobs
    ],
    "stale": [
        "blobs/stale/USR_*.apb"  # Old blob data
    ],
    "user": [
        "blobs/user/USR_*.apb"  # User configuration blobs
    ]
}

# Resource file patterns
RESOURCE_PATTERNS: PatternList = [
    "resources/BaseSystem.dmg",
    "resources/BaseSystem.img",
    "resources/.notices",
    "resources/config.sh"
]

# Boot file patterns
BOOT_PATTERNS: PatternList = [
    "boot/OpenCore.qcow2"  # OpenCore bootloader
]

# OVMF file patterns
OVMF_PATTERNS: PatternList = [
    "ovmf/OVMF_CODE.fd",          # OVMF code
    "ovmf/OVMF_VARS.fd",          # OVMF variables
    "ovmf/user_store/OVMF_VARS.fd" # User OVMF variables
]

# Python bytecode patterns
PYCACHE_PATTERNS: PatternList = [
    "resources/python/__pycache__/*.pyc",
    "resources/python/pypresence/__pycache__/*.pyc"
]

# Script store file patterns
SCRIPT_STORE_PATTERNS: PatternDict = {
    "main": [
        "resources/script_store/.version",
        "resources/script_store/*.py",
        "resources/script_store/*.sh"
    ],
    "extras": [
        "resources/script_store/extras/*.py"
    ],
    "hyperchromiac": [
        "resources/script_store/hyperchromiac/*.py",
        "resources/script_store/hyperchromiac/*.sh"
    ],
    "kunihir0": [
        "resources/script_store/kunihir0/*.py"
    ],
    "kunihir0_utils": [
        "resources/script_store/kunihir0/utils/*.py"
    ],
    "restore": [
        "resources/script_store/restore/*.py"
    ]
}

# Temporary file patterns
TEMP_PATTERNS: PatternList = [
    "*.tmp",
    "*.log",
    "*.bak",
    "tmp/*"
]

# Critical files that should never be deleted during temp cleanup
CRITICAL_FILES: PatternList = [
    "boot/OpenCore.qcow2",     # OpenCore bootloader
    "ovmf/OVMF_CODE.fd",       # UEFI firmware code
    "ovmf/OVMF_VARS.fd",       # UEFI firmware variables
    "resources/script_store/*", # Original project files
    "blobs/user/*"             # User VM configuration
]

# Define cleaner groups for modular cleaning
CLEANER_GROUPS: CleanerGroups = {
    "logs": {
        "name": "Log Files",
        "patterns": LOG_PATTERNS,
        "critical": False
    },
    "main": {
        "name": "Root Directory Files",
        "patterns": ROOT_PATTERNS,
        "critical": False
    },
    "blobs_session": {
        "name": "Session Blob Files",
        "patterns": BLOB_PATTERNS["main"],
        "critical": False
    },
    "blobs_stale": {
        "name": "Stale Blob Files",
        "patterns": BLOB_PATTERNS["stale"],
        "critical": False
    },
    "blobs_user": {
        "name": "User Blob Files",
        "patterns": BLOB_PATTERNS["user"],
        "critical": True  # User blobs are critical
    },
    "resources": {
        "name": "Resource Files",
        "patterns": RESOURCE_PATTERNS,
        "critical": False
    },
    "boot": {
        "name": "Boot Files",
        "patterns": BOOT_PATTERNS,
        "critical": True  # Boot files are critical
    },
    "ovmf": {
        "name": "OVMF Files",
        "patterns": OVMF_PATTERNS,
        "critical": True  # OVMF files are critical
    },
    "pycache": {
        "name": "Python Bytecode Files",
        "patterns": PYCACHE_PATTERNS,
        "critical": False
    },
    "script_store": {
        "name": "Script Store Files",
        "patterns": (SCRIPT_STORE_PATTERNS["main"] + 
                    SCRIPT_STORE_PATTERNS["extras"] +
                    SCRIPT_STORE_PATTERNS["hyperchromiac"] +
                    SCRIPT_STORE_PATTERNS["kunihir0"] +
                    SCRIPT_STORE_PATTERNS["kunihir0_utils"] +
                    SCRIPT_STORE_PATTERNS["restore"]),
        "critical": True  # Script store is critical
    },
    "temp_files": {
        "name": "Temporary Files",
        "patterns": TEMP_PATTERNS,
        "critical": False
    }
}

# All patterns combined for verification
ALL_PATTERNS: PatternList = (
    LOG_PATTERNS +
    ROOT_PATTERNS +
    BLOB_PATTERNS["main"] +
    BLOB_PATTERNS["stale"] +
    BLOB_PATTERNS["user"] +
    RESOURCE_PATTERNS +
    BOOT_PATTERNS +
    OVMF_PATTERNS +
    PYCACHE_PATTERNS +
    SCRIPT_STORE_PATTERNS["main"] +
    SCRIPT_STORE_PATTERNS["extras"] +
    SCRIPT_STORE_PATTERNS["hyperchromiac"] +
    SCRIPT_STORE_PATTERNS["kunihir0"] +
    SCRIPT_STORE_PATTERNS["kunihir0_utils"] +
    SCRIPT_STORE_PATTERNS["restore"] +
    TEMP_PATTERNS
)


def get_safe_patterns(include_critical: bool = False) -> PatternList:
    """Get file patterns that are safe to clean.
    
    Args:
        include_critical: Whether to include critical patterns
        
    Returns:
        List of safe patterns to clean
    """
    safe_patterns: PatternList = []
    
    for group_id, group in CLEANER_GROUPS.items():
        if not group.get("critical", False) or include_critical:
            safe_patterns.extend(group["patterns"])
            
    return safe_patterns


def get_cleanup_tiers() -> Dict[str, Dict[str, Any]]:
    """Get defined cleanup tiers with increasing levels of deletion.
    
    Returns:
        Dictionary of cleanup tiers
    """
    return {
        "safe": {
            "description": "Only cleanup temporary files, logs, and stale blobs",
            "patterns": (LOG_PATTERNS + TEMP_PATTERNS + 
                        BLOB_PATTERNS["stale"] + PYCACHE_PATTERNS)
        },
        "moderate": {
            "description": "Also remove downloaded images and cached data",
            "patterns": (LOG_PATTERNS + TEMP_PATTERNS + 
                        BLOB_PATTERNS["stale"] + BLOB_PATTERNS["main"] +
                        RESOURCE_PATTERNS + PYCACHE_PATTERNS)
        },
        "aggressive": {
            "description": "Remove everything except VM data and essentials",
            "patterns": ALL_PATTERNS,
            "preserve": CRITICAL_FILES
        }
    }


def is_critical_file(pattern: str) -> bool:
    """Check if a file pattern is marked as critical.
    
    Args:
        pattern: File pattern to check
        
    Returns:
        True if pattern is critical, False otherwise
    """
    for group in CLEANER_GROUPS.values():
        if pattern in group["patterns"] and group.get("critical", False):
            return True
            
    return pattern in CRITICAL_FILES


def get_patterns_by_category(category: str) -> PatternList:
    """Get patterns for a specific category.
    
    Args:
        category: Category name
        
    Returns:
        List of patterns for that category
    """
    if category in CLEANER_GROUPS:
        return CLEANER_GROUPS[category]["patterns"]
    
    return []
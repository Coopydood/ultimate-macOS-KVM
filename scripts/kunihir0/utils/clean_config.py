#!/usr/bin/env python3

"""
Configuration for the UMK cleanup utility.
Defines patterns of files to clean in different categories.
"""

# Log file patterns
LOG_PATTERNS = [
    "logs/APC_RUN_*.log"
]

# Main directory file patterns
ROOT_PATTERNS = [
    "BaseSystem.img",
    "boot.sh",
    "HDD.qcow2"
]

# Blob file patterns (in various directories)
BLOB_PATTERNS = {
    "main": [
        "blobs/USR_*.apb"
    ],
    "stale": [
        "blobs/stale/USR_*.apb"
    ],
    "user": [
        "blobs/user/USR_*.apb"
    ]
}

# Resource file patterns
RESOURCE_PATTERNS = [
    "resources/BaseSystem.dmg",
    "resources/BaseSystem.img",
    "resources/.notices",
    "resources/config.sh"
]

# Boot file patterns
BOOT_PATTERNS = [
    "boot/OpenCore.qcow2"
]

# OVMF file patterns
OVMF_PATTERNS = [
    "ovmf/OVMF_CODE.fd",
    "ovmf/OVMF_VARS.fd",
    "ovmf/user_store/OVMF_VARS.fd"
]

# Python bytecode patterns
PYCACHE_PATTERNS = [
    "resources/python/__pycache__/*.pyc",
    "resources/python/pypresence/__pycache__/*.pyc"
]

# Script store file patterns
SCRIPT_STORE_PATTERNS = {
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

# Define cleaner groups for modular cleaning
CLEANER_GROUPS = {
    "logs": {
        "name": "Log Files",
        "patterns": LOG_PATTERNS
    },
    "main": {
        "name": "Root Directory Files",
        "patterns": ROOT_PATTERNS
    },
    "blobs": {
        "name": "Blob Files",
        "patterns": BLOB_PATTERNS["main"] + BLOB_PATTERNS["stale"] + BLOB_PATTERNS["user"]
    },
    "resources": {
        "name": "Resource Files",
        "patterns": RESOURCE_PATTERNS
    },
    "boot": {
        "name": "Boot Files",
        "patterns": BOOT_PATTERNS
    },
    "ovmf": {
        "name": "OVMF Files",
        "patterns": OVMF_PATTERNS
    },
    "pycache": {
        "name": "Python Bytecode Files",
        "patterns": PYCACHE_PATTERNS
    },
    "script_store": {
        "name": "Script Store Files",
        "patterns": (SCRIPT_STORE_PATTERNS["main"] + 
                    SCRIPT_STORE_PATTERNS["extras"] +
                    SCRIPT_STORE_PATTERNS["hyperchromiac"] +
                    SCRIPT_STORE_PATTERNS["kunihir0"] +
                    SCRIPT_STORE_PATTERNS["kunihir0_utils"] +
                    SCRIPT_STORE_PATTERNS["restore"])
    }
}

# All patterns combined for verification
ALL_PATTERNS = (
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
    SCRIPT_STORE_PATTERNS["restore"]
)
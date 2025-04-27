#!/usr/bin/env python3
"""
File Watcher Script

A simple Python script to monitor the project root directory for file additions.
"""

import os
import time
import sys
from pathlib import Path
from datetime import datetime


class FileWatcher:
    """A simple file watcher that monitors a directory for added files."""
    
    def __init__(self, directory_path, interval=2):
        """
        Initialize the file watcher.
        
        Args:
            directory_path: Path to the directory to monitor
            interval: Time interval in seconds between checks
        """
        self.directory_path = Path(directory_path).absolute()
        self.interval = interval
        self.files = set()
        self.running = False
        
        # Initial file scan
        self._scan_files()
        print(f"Watching directory: {self.directory_path}")
        print(f"Initial file count: {len(self.files)}")
        
    def _scan_files(self):
        """Scan the directory and get a set of all files."""
        return set(
            str(file) for file in self.directory_path.glob("**/*") 
            if file.is_file()
        )
    
    def start(self):
        """Start monitoring the directory for changes."""
        self.running = True
        try:
            while self.running:
                current_files = self._scan_files()
                
                # Check for new files
                new_files = current_files - self.files
                if new_files:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n[{timestamp}] New files detected:")
                    for file in sorted(new_files):
                        relative_path = os.path.relpath(file, self.directory_path)
                        print(f"+ {relative_path}")
                    
                    # Update our file set
                    self.files = current_files
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            self.running = False
            print("\nFile watcher stopped.")
    
    def stop(self):
        """Stop the file watcher."""
        self.running = False


if __name__ == "__main__":
    # Default to project root or use command-line argument
    target_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    
    watcher = FileWatcher(target_dir)
    
    print("File watcher started. Press Ctrl+C to stop.")
    watcher.start()
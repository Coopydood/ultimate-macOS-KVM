#!/usr/bin/env python3

"""
Safe ULTMOS uninstaller utility that follows the project coding standards.

This main module provides a unified interface for uninstallation operations
using the safe utility modules.
"""

# --- Standard Library Imports ---
import time
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Set, Union, Tuple, Any
import subprocess # Needed for Popen
import os # For setting environment variables

# --- Add Project Root to sys.path ---
# This allows absolute imports like 'from scripts...' to work when the script is run directly.
try:
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2] # Navigate up from scripts/kunihir0/cleanup.py to project root
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except IndexError:
    print("Error: Could not determine project root. Ensure script is run from within the project structure.", file=sys.stderr)
    sys.exit(1)
# --- End sys.path modification ---

# --- Project-Specific Imports (Using Safe Utils) ---
# Import the centralized logger first
from scripts.kunihir0.utils.logger import default_logger as log, LogLevel, set_log_level

# Import theme manager
from scripts.kunihir0.utils.theme_manager import get_theme_manager, ThemeConfig

# Import safe utilities
from scripts.kunihir0.utils.safe_file_utils import (
    delete_file, ensure_directory_exists, delete_directory_tree,
    read_file_text, is_valid_file, find_files, is_valid_directory,
    create_self_destruct_script # Import the new function
)
from scripts.kunihir0.utils.safe_command_utils import (
    get_user_home, check_command_exists, clear_terminal
)
from scripts.kunihir0.utils.safe_visual_utils import (
    TerminalDisplay, ProgressDisplay, TerminalColor
)

# Import refactored or existing utils (assuming they now use safe methods internally)
from scripts.kunihir0.utils.config_utils import (
    CleanupConfig, UninstallConfig, BlobData, get_critical_files,
    get_cleanup_tiers # Assuming these are still relevant or adapted
)
from scripts.kunihir0.utils.vm_utils import (
    VirtualMachine, find_vms_from_blob_data, remove_vm,
    find_macos_vms # Assuming these are updated
)
from scripts.kunihir0.utils.disk_utils import (
    DiskImage, get_disk_from_blob_data, backup_disk_image,
    delete_disk_image, get_default_backup_dir # Assuming these are updated
)
# clean_config might still be needed for pattern definitions
from scripts.kunihir0.utils.clean_config import (
     CRITICAL_FILES # Import specific needed items
)


class SafeUninstaller:
    """Main uninstaller class that orchestrates cleanup operations safely."""

    def __init__(
        self,
        base_dir: Union[str, Path] = ".",
        config: Optional[UninstallConfig] = None,
    ):
        """Initialize the uninstaller.

        Args:
            base_dir: Base directory of the ULTMOS installation.
            config: Uninstaller configuration.
        """
        log.info(f"Initializing SafeUninstaller for base directory: {base_dir}")
        # Convert to Path
        self.base_dir = Path(base_dir).resolve()

        # Use default config if none provided
        self.config = config or UninstallConfig()
        log.debug(f"Using configuration: {self.config}")

        # Backup dir is now handled by the self-destruct script if needed
        self.config.backup_dir = None # Reset here, not needed by main process

        # Track operations for potential rollback (basic tracking) - Less relevant with self-destruct
        self.operations: List[Dict[str, Any]] = []

        # Try to determine version
        self.version = self._get_ultmos_version()
        log.info(f"Detected ULTMOS version: {self.version}")

    def _get_ultmos_version(self) -> str:
        """Get the ULTMOS version safely."""
        version_file = self.base_dir / ".version"
        content = read_file_text(version_file, quiet=True) # Use safe reader
        if content:
            return content.strip()
        else:
            log.warning(f"Could not read version file at {version_file}")
            return "Unknown"

    def load_blob_data(self) -> BlobData:
        """Load blob data from the blobs directory safely."""
        blob_dir = self.base_dir / "blobs"
        log.debug(f"Loading blob data from: {blob_dir}")
        # BlobData.from_blob_dir should use safe_file_utils internally now
        return BlobData.from_blob_dir(blob_dir)

    def find_vms(self) -> List[VirtualMachine]:
        """Find macOS VMs using blob data and libvirt safely."""
        log.info("Attempting to find macOS VMs...")
        # Find VMs using the recommended function
        vms = find_macos_vms() # Use the non-deprecated function
        log.info(f"Found {len(vms)} potential macOS VMs.")
        return vms

    def find_disk_images(self) -> List[DiskImage]:
        """Find disk images associated with the installation safely."""
        log.info("Attempting to find associated disk images...")
        found_paths: Set[Path] = set()
        disks: List[DiskImage] = []

        # 1. Get disk image from blob data first
        blob_data = self.load_blob_data()
        disk_from_blob = get_disk_from_blob_data(blob_data) # disk_utils is refactored

        if disk_from_blob:
            try:
                # Check existence using safe util before resolving
                if is_valid_file(disk_from_blob.path, quiet=True):
                    abs_path = disk_from_blob.path.resolve() # Resolve only if valid
                    if abs_path not in found_paths:
                        disks.append(disk_from_blob)
                        found_paths.add(abs_path)
                        log.debug(f"Found disk from blob data: {disk_from_blob}")
                else:
                     log.warning(f"Disk path from blob data does not exist or is not a file: {disk_from_blob.path}")
            except Exception as e:
                 log.exception(f"Error resolving disk path from blob data: {disk_from_blob.path}", e)


        # 2. Look for common disk image names in the base directory
        common_patterns = ["*.qcow2", "*.img", "HDD.qcow2", "BaseSystem.img", "BaseSystem.dmg"] # Added dmg
        log.debug(f"Searching for common patterns in {self.base_dir}: {common_patterns}")
        try:
            # Use safe find_files utility
            found_in_base = find_files(self.base_dir, common_patterns, quiet=True)
            for file_path in found_in_base:
                 # Skip OpenCore.qcow2
                 if file_path.name == "OpenCore.qcow2":
                     continue
                 abs_path = file_path.resolve() # Resolve should be safe here
                 if abs_path not in found_paths:
                     # Assume non-physical unless proven otherwise by blob data later
                     # Check if this path matches the one from blob to get physical status
                     is_physical = disk_from_blob is not None and abs_path == disk_from_blob.path.resolve() and disk_from_blob.is_physical
                     disk = DiskImage(file_path, is_physical=is_physical)
                     disks.append(disk)
                     found_paths.add(abs_path)
                     log.debug(f"Found potential disk in base dir: {disk}")
        except Exception as e:
            log.exception(f"Error searching for common disk patterns in {self.base_dir}", e)


        # 3. Additionally check the 'disks' subdirectory if it exists
        disks_dir = self.base_dir / "disks"
        if is_valid_directory(disks_dir, quiet=True): # Use safe check
             log.debug(f"Searching for common patterns in {disks_dir}...")
             try:
                 found_in_disks_dir = find_files(disks_dir, common_patterns, quiet=True)
                 for file_path in found_in_disks_dir:
                      abs_path = file_path.resolve()
                      if abs_path not in found_paths:
                          is_physical = disk_from_blob is not None and abs_path == disk_from_blob.path.resolve() and disk_from_blob.is_physical
                          disk = DiskImage(file_path, is_physical=is_physical)
                          disks.append(disk)
                          found_paths.add(abs_path)
                          log.debug(f"Found potential disk in disks dir: {disk}")
             except Exception as e:
                 log.exception(f"Error searching for common disk patterns in {disks_dir}", e)
        else:
             log.debug(f"Disks subdirectory not found or invalid: {disks_dir}")

        log.info(f"Found {len(disks)} unique disk images.")
        return disks

    def clean_temporary_files(self) -> int:
        """Clean temporary files safely using safe utilities."""
        log.info("Starting temporary file cleanup...")
        # Get critical file patterns that should be preserved
        # Assuming get_critical_files is safe or defined in config_utils
        try:
            critical_patterns = get_critical_files()
        except NameError: # Fallback if function removed/renamed
             log.warning("get_critical_files function not found, using default critical patterns.")
             critical_patterns = CRITICAL_FILES # Use imported constant

        # Define patterns to clean (consider moving this to config_utils or clean_config)
        # Define patterns for truly temporary/safe files
        patterns_to_clean = [
            "*.log",             # Log files in the root
            "logs/*.log",        # Log files in the logs/ directory
            "*.tmp",             # Temporary files in the root
            "tmp/*",             # Files within a potential tmp/ directory
            "blobs/stale/*.apb"  # Only stale blobs
            # Removed "blobs/*.apb" to avoid accidentally targeting user blobs or other critical blobs
        ]
        log.debug(f"Cleaning patterns (safe temp only): {patterns_to_clean}")
        log.debug(f"Preserving patterns: {critical_patterns}")

        # Find files matching patterns using safe_file_utils.find_files
        all_matching_files = find_files(self.base_dir, patterns_to_clean, quiet=False) # Log errors finding files

        files_to_clean: Set[Path] = set()
        for file_path in all_matching_files:
            try:
                # Check if file should be preserved
                should_preserve = False
                abs_file_path = file_path.resolve() # Resolve should be safe

                # Check against critical patterns (using Path.match)
                for preserve_pattern_str in critical_patterns:
                    # Construct absolute pattern path for matching
                    # Handle potential errors if preserve_pattern_str is invalid
                    try:
                        # Need to handle glob patterns correctly relative to base_dir
                        # Example: blobs/user/* should match /path/to/base_dir/blobs/user/file.apb
                        # Path.match works relative to the Path object itself if pattern is relative
                        # If preserve pattern is relative, match against path relative to base_dir
                        if not Path(preserve_pattern_str).is_absolute():
                             relative_file_path = abs_file_path.relative_to(self.base_dir)
                             if relative_file_path.match(preserve_pattern_str):
                                 should_preserve = True
                                 log.debug(f"Preserving file {file_path} due to pattern {preserve_pattern_str}")
                                 break
                        # If preserve pattern is absolute (less likely needed)
                        elif abs_file_path.match(preserve_pattern_str):
                             should_preserve = True
                             log.debug(f"Preserving file {file_path} due to absolute pattern {preserve_pattern_str}")
                             break
                    except ValueError: # If relative_to fails (path not inside base_dir)
                         pass # Don't preserve if path isn't relative
                    except Exception as e_match:
                         log.warning(f"Error matching preserve pattern '{preserve_pattern_str}' for file {file_path}: {e_match}")

                if not should_preserve:
                    files_to_clean.add(file_path)

            except Exception as e_resolve:
                 log.error(f"Error resolving or checking file {file_path}", e_resolve)


        files_to_clean_list = sorted(list(files_to_clean))
        log.info(f"Found {len(files_to_clean_list)} temporary files to potentially clean.")

        # Confirm with user if needed
        if self.config.confirm_actions and files_to_clean_list:
            tm = get_theme_manager()
            tm.display_step(f"Found {len(files_to_clean_list)} temporary files to clean:", "info")
            for file_path in files_to_clean_list[:5]:  # Show only first 5
                try:
                    tm.display_step(f"  - {file_path.relative_to(self.base_dir)}", "info")
                except ValueError:
                    tm.display_step(f"  - {file_path}", "info") # Print absolute if not relative

            if len(files_to_clean_list) > 5:
                tm.display_step(f"  ... and {len(files_to_clean_list) - 5} more", "info")

            if not self._confirm_action("Clean these temporary files?"):
                log.info("Skipping temporary file cleanup.")
                return 0

        # Clean files
        cleaned_count = 0
        for file_path in files_to_clean_list:
            if self.config.dry_run:
                log.info(f"[Dry Run] Would delete: {file_path}")
                cleaned_count += 1
            else:
                # Use safe delete function
                if delete_file(file_path, quiet=False): # Log success/failure
                    cleaned_count += 1
                    # Track operation
                    self.operations.append({
                        "type": "delete_file",
                        "path": str(file_path), # Store as string for serialization if needed
                        "timestamp": time.time()
                    })

        log.info(f"Temporary file cleanup finished. Cleaned {cleaned_count} files.")
        return cleaned_count

    def remove_vms(self) -> int:
        """Remove VMs safely using vm_utils."""
        log.info("Starting VM removal process...")
        vms = self.find_vms() # Uses safe find internally

        if not vms:
            log.info("No macOS VMs found to remove.")
            return 0

        # Confirm with user if needed (This confirmation is now handled in run_menu)
        # if self.config.confirm_actions:
        #     TerminalDisplay.print_step(f"Found {len(vms)} macOS VMs:", "info")
        #     for vm in vms:
        #         print(f"  - {vm}") # Uses VM __str__ method
        #     if not self._confirm_action("Remove these VMs?"):
        #         log.info("Skipping VM removal.")
        #         return 0

        # Remove VMs
        removed_count = 0
        for vm in vms:
            # Always call remove_vm, passing the dry_run status
            log.info(f"{'Simulating removal of' if self.config.dry_run else 'Removing'} VM: {vm.name}")
            # backup_dir is None for this operation

            # Add progress display for better UX using theme manager
            get_theme_manager().display_progress(f"{'Simulating removal of' if self.config.dry_run else 'Removing'} {vm.name}...", 0.5)

            # Call remove_vm from vm_utils, passing dry_run status
            # remove_vm now handles the dry-run logic internally for files
            # Explicitly pass backup_dir=None for this operation
            if remove_vm(
                vm,
                keep_disks=self.config.keep_disks, # keep_disks affects --remove-all-storage flag in undefine
                backup_dir=None, # Don't backup XML for "Remove VMs only"
                dry_run=self.config.dry_run # Pass dry_run status
            ):
                removed_count += 1
                # Track operation only if not dry run? Or track simulation?
                # For now, let's track even simulations for consistency in count
                # but maybe add a flag later if needed.
                if not self.config.dry_run: # Only track actual operations
                    self.operations.append({
                        "type": "remove_vm",
                        "vm_name": vm.name,
                        "timestamp": time.time()
                    })
                # remove_vm handles its own logging of success/failure

        log.info(f"VM removal finished. Removed {removed_count} VMs.")
        return removed_count

    def handle_disk_images(self) -> int:
        """Handle disk images based on configuration using safe disk_utils."""
        log.info("Starting disk image handling...")
        disks = self.find_disk_images() # Uses safe find internally

        if not disks:
            log.info("No disk images found to handle.")
            return 0

        # Confirm with user if needed (This confirmation is now handled in run_menu)
        # if self.config.confirm_actions:
        #     TerminalDisplay.print_step(f"Found {len(disks)} disk images:", "info")
        #     for disk in disks:
        #         print(f"  - {disk}") # Uses DiskImage __str__ method
        #     action = "backup" if self.config.keep_disks else "delete"
        #     if not self._confirm_action(f"{action.capitalize()} these disk images?"):
        #         log.info("Skipping disk image handling.")
        #         return 0

        # Handle disk images
        handled_count = 0
        for disk in disks:
            # Never process physical disks (check handled in disk_utils)
            if disk.is_physical:
                 log.warning(f"SAFETY: Skipping physical disk {disk.path}")
                 continue

            if self.config.keep_disks:
                # Backup the disk
                if self.config.dry_run:
                    # Need backup_dir even for dry run log message
                    # Generate default backup dir path for logging if not set
                    backup_dir_path = self.config.backup_dir or (Path.home() / "ultmos_backups_DRYRUN")
                    log.info(f"[Dry Run] Would backup: {disk.path} to {backup_dir_path}")
                    handled_count += 1
                else:
                    # Ensure backup dir is set before actual backup
                    if not self.config.backup_dir:
                         try:
                              self.config.backup_dir = get_default_backup_dir()
                              log.info(f"Generated default backup directory: {self.config.backup_dir}")
                         except Exception as e:
                              log.error("Failed to determine backup directory. Cannot backup disk.", e)
                              continue # Skip this disk if backup dir fails
                    log.info(f"Backing up disk image: {disk.path}")
                    # backup_disk_image from disk_utils should be safe now
                    backup_path = backup_disk_image(
                        disk,
                        self.config.backup_dir,
                        quiet=False # Log details
                    )
                    if backup_path:
                        handled_count += 1
                        # Track operation
                        self.operations.append({
                            "type": "backup_disk",
                            "source": str(disk.path),
                            "destination": str(backup_path),
                            "timestamp": time.time()
                        })
            else:
                # Delete the disk
                if self.config.dry_run:
                    log.info(f"[Dry Run] Would delete: {disk.path}")
                    handled_count += 1
                else:
                    log.info(f"Deleting disk image: {disk.path}")
                    # delete_disk_image from disk_utils should be safe now
                    if delete_disk_image(disk, quiet=False): # Log details
                        handled_count += 1
                        # Track operation
                        self.operations.append({
                            "type": "delete_disk",
                            "path": str(disk.path),
                            "timestamp": time.time()
                        })

        log.info(f"Disk image handling finished. Handled {handled_count} images.")
        return handled_count

    def uninstall_everything(self) -> bool:
        """Completely uninstall ULTMOS safely using a self-destruct script."""
        log.warning("Starting complete uninstallation process...")

        # Confirm with user
        if self.config.confirm_actions:
            tm = get_theme_manager()
            tm.display_step("⚠ WARNING: This will completely uninstall ULTMOS", "warning")
            tm.display_step("  - All VMs will be removed from libvirt (if found)", "warning")
            action = "backed up" if self.config.keep_disks else "deleted"
            tm.display_step(f"  - Disk images will be {action}", "warning")
            tm.display_step(f"  - The entire ULTMOS directory ({self.base_dir}) will be deleted", "warning")

            # This is a critical operation, require confirmation
            if not self._confirm_action("Proceed with complete uninstallation?", is_critical=True):
                log.info("Uninstallation cancelled by user.")
                return False

        # 1. Find VMs to include in the self-destruct script
        vms = self.find_vms()
        vm_names = [vm.name for vm in vms]
        log.info(f"VMs identified for self-destruct script: {vm_names}")

        # 2. Handle disk image backups *before* creating the script if keep_disks is True
        #    Deletion will happen inside the self-destruct script if keep_disks is False.
        if self.config.keep_disks:
             log.info("Handling disk image backups before initiating self-destruct...")
             # Backup dir generation/check is now handled within the self-destruct script itself
             # We still call handle_disk_images here to perform the actual backup *now*
             self.handle_disk_images() # This will perform backups if keep_disks=True
        else:
             log.info("Disk images will be deleted by the self-destruct script.")

        # --- Prompt for Self-Destruct Visual Mode ---
        tm = get_theme_manager()
        log.info("Prompting user for self-destruct visual mode.")
        
        prompt_title = "Self-Destruct Visuals"
        prompt_lines = [
            "How would you like the final cleanup process to look?",
            "1. Full Pretty Mode (Rich animations and visual effects)",
            "2. Minimal Mode (All information, but with simpler, faster visuals; still colorful)"
        ]
        
        # Display prompt using theme manager for consistency if possible, or simple input
        # For simplicity here, using direct input with color, assuming theme_manager might not have a direct 2-choice prompt.
        # A more integrated approach would use theme_manager.get_user_choice if it supports this format.
        
        print("\n" + TerminalColor.colorize(prompt_title, "bright_yellow"))
        for line in prompt_lines:
            print(TerminalColor.colorize(f"  {line}", "default"))
        
        visual_mode_choice = ""
        while visual_mode_choice not in ["1", "2"]:
            try:
                visual_mode_choice = input(TerminalColor.colorize("Enter your choice (1/2): ", "bright_cyan")).strip()
                if visual_mode_choice not in ["1", "2"]:
                    print(TerminalColor.colorize("Invalid choice. Please enter 1 or 2.", "bright_red"))
            except EOFError:
                log.warning("EOF received, defaulting to Full Pretty Mode for self-destruct.")
                visual_mode_choice = "1" # Default to full on EOF
                break
            except KeyboardInterrupt:
                log.warning("User cancelled visual mode selection, defaulting to Full Pretty Mode for self-destruct.")
                print("\nDefaulting to Full Pretty Mode.")
                visual_mode_choice = "1" # Default to full on Ctrl+C
                break

        if visual_mode_choice == "2":
            os.environ['ULTMOS_SELF_DESTRUCT_MODE'] = 'minimal'
            log.info("Minimal visual mode selected for self-destruct.")
            tm.display_step("Minimal Mode selected for final cleanup.", "info")
        else:
            os.environ['ULTMOS_SELF_DESTRUCT_MODE'] = 'full'
            log.info("Full Pretty visual mode selected for self-destruct.")
            tm.display_step("Full Pretty Mode selected for final cleanup.", "info")
        
        time.sleep(0.5) # Brief pause after selection

        # 3. Create and execute the self-destruct script
        script_path = create_self_destruct_script(
            directory_to_delete=self.base_dir,
            keep_disks=self.config.keep_disks,
            vm_names=vm_names,
            quiet=False # Log script creation details
        )

        if not script_path:
            log.critical("Failed to create the self-destruct script. Aborting uninstallation.")
            return False

        if self.config.dry_run:
            log.info(f"[Dry Run] Would execute self-destruct script: sudo python3 {script_path} --directory {self.base_dir} --keep-disks {self.config.keep_disks} --vms {' '.join(vm_names)}")
            # Optionally try to delete the temp script even in dry run? Or leave it?
            # Let's leave it for inspection for now.
            # try:
            #     Path(script_path).unlink()
            # except OSError:
            #     pass
            return True # Simulate success
        else:
            try:
                log.warning(f"Executing self-destruct script: sudo python3 {script_path} ...")
                log.warning("Opening a terminal window to show the cleanup progress...")
                log.warning("You may be prompted for your sudo password in the new terminal window.")

                # Construct the command to execute the python script with sudo
                cmd = ['sudo', 'python3', script_path,
                       '--directory', str(self.base_dir),
                       '--keep-disks', str(self.config.keep_disks)]
                if vm_names:
                    cmd.append('--vms')
                    cmd.extend(vm_names)

                # Launch the script in a visible terminal so user can see progress and animations
                # The terminal will stay open after this script exits
                terminal_cmd = ['x-terminal-emulator', '-e', ' '.join(['sudo', 'python3', str(script_path),
                               '--directory', str(self.base_dir),
                               '--keep-disks', str(self.config.keep_disks),
                               '--vms'] + vm_names)]
                
                # Alternative terminal commands for different systems
                if not check_command_exists('x-terminal-emulator', quiet=True):
                    if check_command_exists('gnome-terminal', quiet=True):
                        terminal_cmd = ['gnome-terminal', '--', 'sudo', 'python3', str(script_path),
                                       '--directory', str(self.base_dir),
                                       '--keep-disks', str(self.config.keep_disks),
                                       '--vms'] + vm_names
                    elif check_command_exists('kgx', quiet=True):
                        terminal_cmd = ['kgx', '--', 'sudo', 'python3', str(script_path),
                                       '--directory', str(self.base_dir),
                                       '--keep-disks', str(self.config.keep_disks),
                                       '--vms'] + vm_names
                    elif check_command_exists('konsole', quiet=True):
                        terminal_cmd = ['konsole', '-e', 'sudo python3 ' + str(script_path) +
                                       ' --directory ' + str(self.base_dir) +
                                       ' --keep-disks ' + str(self.config.keep_disks) +
                                       ' --vms ' + ' '.join(vm_names)]
                    elif check_command_exists('xterm', quiet=True):
                        terminal_cmd = ['xterm', '-e', 'sudo python3 ' + str(script_path) +
                                       ' --directory ' + str(self.base_dir) +
                                       ' --keep-disks ' + str(self.config.keep_disks) +
                                       ' --vms ' + ' '.join(vm_names)]
                    else:
                        # Fallback if no terminal is found
                        log.warning("No suitable terminal emulator found. Running without visible output.")
                        process = subprocess.Popen(cmd)
                        log.info(f"Self-destruct script launched with PID: {process.pid}")
                        # Do NOT track this operation here, as it happens after exit
                        return True
                
                log.info(f"Launching self-destruct script in a new terminal window...")
                process = subprocess.Popen(terminal_cmd)
                # Do NOT track this operation here, as it happens after exit
                return True # Return True assuming the script launch was successful
            except Exception as e:
                log.critical(f"Failed to launch self-destruct script {script_path}", e)
                # Clean up the script if launch fails
                try:
                    Path(script_path).unlink()
                except OSError:
                    pass
                return False


    def _confirm_action(self, prompt: str, timeout: Optional[int] = None, is_critical: bool = False) -> bool:
        """Prompt the user for confirmation using theme manager."""
        # Use theme manager for prompts
        theme_manager = get_theme_manager()
        color = "bright_yellow" # Use string name
        extra_prompt = "(y/n): "

        if self.config.dry_run: # Accessing dry_run status from self.config
            prompt = f"[Dry Run] {prompt}"
            color = "bright_cyan" # Change color for dry run prompts to be less alarming

        if is_critical:
             # For critical actions in dry run, still indicate it's a simulated critical action
             critical_color = "bright_magenta" if self.config.dry_run else "bright_red"
             prompt = f"{prompt} THIS IS {'NORMALLY ' if self.config.dry_run else ''}IRREVERSIBLE!"
             extra_prompt = "Type 'yes' to confirm: "
             color = critical_color # Override color for critical prompts

        # Format prompt with appropriate color and style based on theme
        if theme_manager.get_theme_name() == "animated":
            # In animated theme, we'll display the prompt using theme_manager
            theme_manager.display_step(prompt, "warning" if not is_critical else "error")
            full_prompt = extra_prompt
        else:
            # In standard theme, we'll use the combined prompt
            full_prompt = TerminalColor.colorize(prompt, color) + extra_prompt

        # Basic timeout implementation (no select/async needed for simple CLI)
        start_time = time.time()
        response = ""
        try:
            if timeout:
                 print(f"{full_prompt} (waiting {timeout}s)", end="")
                 sys.stdout.flush()
                 # This is a blocking wait, not ideal but simple
                 # A more robust solution would use select or threading
                 # For now, just check elapsed time after input
                 response = input().strip().lower()
                 if time.time() - start_time > timeout:
                      print("\nTimeout elapsed. Assuming 'no'.")
                      return False
            else:
                 response = input(full_prompt).strip().lower()

            if is_critical:
                 return response == 'yes'
            else:
                 return response in ['y', 'yes']
        except KeyboardInterrupt:
             print("\nConfirmation cancelled.")
             return False
        except EOFError: # Handle case where input stream is closed
             print("\nInput stream closed. Assuming 'no'.")
             return False


def run_menu(uninstaller: SafeUninstaller) -> int:
    """Run the interactive uninstaller menu using the theme manager."""
    # Get the theme manager instance
    theme_manager = get_theme_manager()
    
    while True:
        # Define menu options
        options = [
            {"title": "Show detected components", "description": "Display all VMs and disk images", "color": "bright_cyan"},
            {"title": "Remove VMs only", "description": "Remove VMs but keep disk images", "color": "bright_yellow"},
            {"title": "Clean temporary files only", "description": "Remove temporary log files and cache", "color": "bright_blue"},
            {"title": "Clean VMs and temporary files", "description": "Remove VMs and clean temporary files", "color": "bright_magenta"},
            {"title": "Uninstall but keep disks", "description": "Remove ULTMOS but backup disk images", "color": "bright_red"},
            {"title": "Uninstall everything", "description": "Completely remove ULTMOS and all data", "color": "bright_red"},
            
            # Toggle options
            {"title": f"Toggle dry run mode ({('ON' if uninstaller.config.dry_run else 'OFF')})",
             "description": "Simulate operations without making changes",
             "color": "bright_green" if uninstaller.config.dry_run else "bright_black"},
            
            {"title": f"Toggle theme ({theme_manager.get_theme_display_name()})",
             "description": "Switch between standard and animated theme",
             "color": "bright_cyan"},
            
            {"title": "Return to main menu", "description": "Go back to ULTMOS main menu", "color": "bright_green"},
            {"title": "Exit", "description": "Exit the uninstaller", "color": "bright_cyan"}
        ]
        
        # Define menu content
        title = "ULTMOS Safe Uninstaller"
        subheading = "Safely remove ULTMOS components"
        body_lines = [
            "This utility helps you safely remove ULTMOS components from your system.",
            "You can remove VMs, clean temporary files, or uninstall everything.",
            "Use with caution - some operations cannot be undone.",
            f"ULTMOS Version: {uninstaller.version} - Safe Uninstaller by kunihir0"
        ]
        
        # Display the menu using the theme manager
        theme_manager.display_menu(title, subheading, body_lines, options)
        
        # Get user choice using the theme manager
        try:
            choice = theme_manager.get_user_choice("Select option")
        except EOFError:
            log.warning("Input stream closed, exiting menu.")
            return 1  # Indicate error/exit

        # Accept various exit options
        if choice in ["0", "10"] or choice.lower() in ["exit", "q", "quit"]:
            theme_manager.display_step("Exiting uninstaller", "success")
            return 0

        elif choice == "1":
            theme_manager.clear_screen()
            theme_manager.print_banner("Detected Components")
            # Show VMs
            theme_manager.display_step("Detected VMs:", "info")
            vms = uninstaller.find_vms() # Safe call
            if vms:
                for vm in vms:
                    theme_manager.display_step(f"  - {vm}", "info") # Relies on VM __str__
            else:
                theme_manager.display_step("No macOS VMs found", "warning")

            # Show disk images
            theme_manager.display_step("\nDetected disk images:", "info")
            disks = uninstaller.find_disk_images() # Safe call
            if disks:
                theme_manager.display_step(f"Total disk images found: {len(disks)}", "info")
                for disk in disks:
                     theme_manager.display_step(f"  - {disk}", "info") # Relies on DiskImage __str__
            else:
                theme_manager.display_step("  No disk images found", "warning")

            theme_manager.get_user_choice("Press Enter to continue")

        elif choice == "2":
            theme_manager.clear_screen()
            theme_manager.print_banner("Remove VMs Only")
            theme_manager.display_progress("Detecting VMs...", 0.5)
            vms = uninstaller.find_vms()
            if not vms:
                theme_manager.display_step("No macOS VMs found", "warning")
            else:
                theme_manager.display_step(f"Found {len(vms)} VMs:", "info")
                files_to_remove: List[Path] = []
                disks_associated: List[Path] = []
                for vm in vms:
                    theme_manager.display_step(f"  - {vm}", "info") # Prints VM name and state
                    # Collect associated files that exist
                    if vm.script_path and vm.script_path.exists():
                        files_to_remove.append(vm.script_path)
                    # Check vm.xml_path which might be None or not exist
                    if vm.xml_path and vm.xml_path.exists():
                         files_to_remove.append(vm.xml_path)
                    # Collect associated disk paths
                    for disk_path in vm.disk_paths:
                         if disk_path.exists(): # Check if disk exists
                              disks_associated.append(disk_path)


                # Display files to be removed if any were found
                if files_to_remove:
                     theme_manager.display_step("\nAssociated configuration files to be removed:", "warning")
                     unique_files = sorted(list(set(files_to_remove))) # Ensure uniqueness and sort
                     for file_path in unique_files:
                          try:
                               # Try to display relative path for clarity
                               theme_manager.display_step(f"  - {file_path.relative_to(uninstaller.base_dir)}", "info")
                          except ValueError:
                               # Fallback to absolute path if not relative
                               theme_manager.display_step(f"  - {file_path}", "info")

                # Display associated disk files (these are NOT removed by this option)
                if disks_associated:
                     theme_manager.display_step("\nAssociated disk images (NOT removed by this option):", "info")
                     unique_disks = sorted(list(set(disks_associated)))
                     for disk_path in unique_disks:
                          try:
                               theme_manager.display_step(f"  - {disk_path.relative_to(uninstaller.base_dir)}", "info")
                          except ValueError:
                               theme_manager.display_step(f"  - {disk_path}", "info")


                # Update confirmation prompts
                if uninstaller._confirm_action("Do you want to remove the disk images as well?"):
                    uninstaller.config.keep_disks = False
                    log.info("Disk images will be deleted along with VM definitions.")
                else:
                    uninstaller.config.keep_disks = True
                    log.info("Disk images will be preserved.")

                if uninstaller._confirm_action("Proceed with VM removal?"):
                    removed = uninstaller.remove_vms() # Safe call, logs internally
                    # Log final summary here
                    keep_status = "preserved" if uninstaller.config.keep_disks else "deleted"
                    log.info(f"VM removal operation completed. Removed {removed} VMs, disk images {keep_status}.")
                else:
                    log.info("VM removal cancelled.")
            theme_manager.get_user_choice("Press Enter to continue")

        elif choice == "3":
            theme_manager.clear_screen()
            theme_manager.print_banner("Clean Temporary Files")
            theme_manager.display_progress("Scanning for temporary files...", 0.5)
            cleaned = uninstaller.clean_temporary_files() # Safe call, logs internally
            # Log final summary here
            log.info(f"Temporary file cleanup operation completed. Cleaned {cleaned} files.")
            theme_manager.get_user_choice("Press Enter to continue")
            
        elif choice == "4":
            theme_manager.clear_screen()
            theme_manager.print_banner("Clean VMs and Temporary Files")
            
            # First handle VM removal
            theme_manager.display_progress("Detecting VMs...", 0.5)
            vms = uninstaller.find_vms()
            if vms:
                theme_manager.display_step(f"Found {len(vms)} VMs:", "info")
                files_to_remove: List[Path] = []
                disks_associated: List[Path] = []
                for vm in vms:
                    theme_manager.display_step(f"  - {vm}", "info")
                    # Collect associated files that exist
                    if vm.script_path and vm.script_path.exists():
                        files_to_remove.append(vm.script_path)
                    if vm.xml_path and vm.xml_path.exists():
                        files_to_remove.append(vm.xml_path)
                    # Collect associated disk paths
                    for disk_path in vm.disk_paths:
                        if disk_path.exists():
                            disks_associated.append(disk_path)
                
                if disks_associated:
                    theme_manager.display_step(f"\nFound {len(disks_associated)} disk images:", "info")
                    unique_disks = sorted(list(set(disks_associated)))
                    for disk_path in unique_disks[:5]:
                        try:
                            theme_manager.display_step(f"  - {disk_path.relative_to(uninstaller.base_dir)}", "info")
                        except ValueError:
                            theme_manager.display_step(f"  - {disk_path}", "info")
                    if len(unique_disks) > 5:
                        theme_manager.display_step(f"  ... and {len(unique_disks) - 5} more", "info")
                
                # Ask about disk removal
                if uninstaller._confirm_action("Do you want to remove the disk images as well?"):
                    uninstaller.config.keep_disks = False
                    log.info("Disk images will be deleted along with VM definitions.")
                else:
                    uninstaller.config.keep_disks = True
                    log.info("Disk images will be preserved.")
                
                if uninstaller._confirm_action("Proceed with VM removal?"):
                    removed = uninstaller.remove_vms()
                    keep_status = "preserved" if uninstaller.config.keep_disks else "deleted"
                    log.info(f"VM removal operation completed. Removed {removed} VMs, disk images {keep_status}.")
                else:
                    log.info("VM removal cancelled.")
            else:
                theme_manager.display_step("No macOS VMs found", "warning")
            
            # Then handle temporary file cleanup
            theme_manager.display_step("\nProceeding with temporary file cleanup...", "info")
            theme_manager.display_progress("Scanning for temporary files...", 0.5)
            cleaned = uninstaller.clean_temporary_files()
            log.info(f"Temporary file cleanup operation completed. Cleaned {cleaned} files.")
            
            theme_manager.get_user_choice("Press Enter to continue")

        elif choice == "5":
            theme_manager.clear_screen()
            theme_manager.print_banner("Uninstall (Keep Disks)")
            if uninstaller.config.dry_run:
                theme_manager.display_step("DRY RUN MODE: No actual changes will be made.", "success")
            theme_manager.display_step("WARNING: This will remove ULTMOS but keep/backup disks.", "warning")
            # Backup dir is determined/shown by self-destruct script if needed
            # TerminalDisplay.print_step(f"Disk images will be backed up to: {uninstaller.config.backup_dir}", "info")

            vms = uninstaller.find_vms()
            if vms:
                theme_manager.display_step(f"Found {len(vms)} VMs whose definitions will be removed:", "warning")
                for vm in vms:
                    theme_manager.display_step(f"  - {vm.name}", "info")

            theme_manager.display_step("This operation cannot be undone!", "warning")
            # Confirmation is now handled within uninstaller.uninstall_everything()
            log.info("Preparing for uninstallation (keeping disks)...")
            uninstaller.config.keep_disks = True # Ensure this is set before calling
            success = uninstaller.uninstall_everything() # This will handle its own confirmation

            if success:
                log.success("Self-destruct script initiated successfully. Exiting.")
                return 0 # Exit after successful initiation
            else:
                # This branch is reached if uninstall_everything returns False (cancelled by user or failed).
                # Specific reasons (cancelled/failed) are logged within uninstall_everything.
                log.warning("Uninstallation (keeping disks) was not completed.")
            theme_manager.get_user_choice("Press Enter to continue")

        elif choice == "6":
            theme_manager.clear_screen()
            theme_manager.print_banner("Uninstall EVERYTHING")
            if uninstaller.config.dry_run:
                theme_manager.display_step("DRY RUN MODE: No actual changes will be made.", "success")
            theme_manager.display_step("WARNING: This will completely remove ULTMOS", "error")
            theme_manager.display_step("ALL YOUR VM DISK IMAGES WILL BE PERMANENTLY DELETED (if not in dry run)!", "error")

            vms = uninstaller.find_vms()
            if vms:
                theme_manager.display_step(f"Found {len(vms)} VMs whose definitions will be removed:", "warning")
                for vm in vms:
                    theme_manager.display_step(f"  - {vm.name}", "info")
            disks = uninstaller.find_disk_images()
            if disks:
                theme_manager.display_step(f"Found {len(disks)} disk images to DELETE:", "error")
                for disk in disks[:5]:
                    theme_manager.display_step(f"  - {disk.path.name} ({disk.size_human})", "error")
                if len(disks) > 5:
                    theme_manager.display_step(f"  - ... and {len(disks) - 5} more", "error")

            theme_manager.display_step("THIS OPERATION CANNOT BE UNDONE!", "error")
            # Confirmation is now handled within uninstaller.uninstall_everything()
            log.info("Preparing for complete uninstallation...")
            uninstaller.config.keep_disks = False # Ensure this is set before calling
            success = uninstaller.uninstall_everything() # This will handle its own confirmation

            if success:
                log.success("Self-destruct script initiated successfully. Exiting.")
                return 0 # Exit after successful initiation
            else:
                # This branch is reached if uninstall_everything returns False (cancelled by user or failed).
                # Specific reasons (cancelled/failed) are logged within uninstall_everything.
                log.warning("Complete uninstallation was not completed.")
            theme_manager.get_user_choice("Press Enter to continue")

        elif choice == "7":
            uninstaller.config.dry_run = not uninstaller.config.dry_run
            status = "enabled" if uninstaller.config.dry_run else "disabled"
            theme_manager.display_step(f"Dry run mode {status}", "success")
            time.sleep(1)
            
        elif choice == "8":
            new_theme = theme_manager.toggle_theme()
            theme_manager.display_step(f"Theme switched to {theme_manager.get_theme_display_name()}", "success")
            time.sleep(1)
            
        elif choice == "9" or choice.lower() in ["m", "main"]:
            theme_manager.display_step("Returning to main menu...", "success")
            time.sleep(1)
            # When run directly without being imported from extras.py, return to main menu
            # Otherwise just exit and let the parent script handle it
            if __name__ == "__main__":
                # Use subprocess instead of os.system for better process handling
                import subprocess
                subprocess.run([sys.executable, './main.py'], check=True)
            return 0  # Exit the current script

        else:
            theme_manager.display_step("Invalid selection", "error")
            time.sleep(1)

    return 0 # Should not be reached


def main() -> int:
    """Main entry point for the safe uninstaller."""
    # Setup basic argument parsing
    parser = argparse.ArgumentParser(
        description="ULTMOS Safe Uninstaller",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--base-dir", type=Path, default=".",
        help="Base directory of the ULTMOS installation (default: current directory)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Skip all confirmation prompts (USE WITH CAUTION!)"
    )
    parser.add_argument(
        "--keep-disks", action="store_true",
        help="Keep/backup disk images during full uninstall"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simulate operations without making changes"
    )
    parser.add_argument(
        "--temp-only", action="store_true",
        help="Clean only temporary files and exit"
    )
    parser.add_argument(
        "--vm-only", action="store_true",
        help="Remove only VMs and exit"
    )
    parser.add_argument(
        "--theme", choices=[ThemeConfig.THEME_STANDARD, ThemeConfig.THEME_ANIMATED], default=ThemeConfig.THEME_STANDARD,
        help="Select theme for display (standard or animated)"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Enable quiet mode for animations (reduced visual effects)"
    )
    parser.add_argument(
        "--log-level", choices=[level.name for level in LogLevel], default="INFO",
        help="Set the minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    parser.add_argument(
        "--no-color", action="store_true",
        help="Disable colored output"
    )
    args = parser.parse_args()

    # Configure logger
    try:
        log_level = LogLevel[args.log_level.upper()]
        set_log_level(log_level)
    except KeyError:
        log.error(f"Invalid log level: {args.log_level}. Using INFO.")
        set_log_level(LogLevel.INFO)

    # Configure theme manager with command line arguments
    theme_manager = get_theme_manager()
    
    # Set theme based on command line args
    theme_manager.config.set_theme(args.theme)
    log.info(f"Using theme: {theme_manager.get_theme_display_name()}")
    
    # Configure quiet mode if specified
    if args.quiet:
        if not theme_manager.is_quiet_mode():  # Only toggle if not already in quiet mode
            theme_manager.toggle_quiet_mode()
        log.info(f"Quiet mode enabled for animations: {theme_manager.is_quiet_mode()}")
    
    # Handle color settings
    if args.no_color:
        # Disable colors in the logger (assuming logger has this capability)
        # Need to implement this in logger.py if not already present
        # log.use_colors(False) # Example call
        log.info("Color output disabled")

    log.info("ULTMOS Safe Uninstaller starting...")
    log.debug(f"Command line arguments: {args}")

    try:
        # Determine base directory
        base_dir = args.base_dir.resolve()
        if not is_valid_directory(base_dir, quiet=False):
             log.critical(f"Invalid base directory specified: {args.base_dir}")
             return 1

        # Set up configuration
        config = UninstallConfig(
            keep_disks=args.keep_disks,
            clean_temp=True, # Assume always clean temp unless specific flag added
            remove_vms=True, # Assume always remove VMs unless specific flag added
            confirm_actions=not args.force,
            dry_run=args.dry_run,
            backup_dir=None # Let constructor handle default
        )

        # Create uninstaller instance
        uninstaller = SafeUninstaller(base_dir, config)

        # Handle specific command-line operations first
        if args.temp_only:
            log.info("Executing temporary file cleanup only...")
            cleaned = uninstaller.clean_temporary_files()
            log.success(f"Temporary file cleanup finished. Cleaned {cleaned} files.")
            return 0
        elif args.vm_only:
            log.info("Executing VM removal only...")
            removed = uninstaller.remove_vms()
            log.success(f"VM removal finished. Removed {removed} VMs.")
            return 0
        # Add logic here if a full uninstall is triggered by args, e.g., --uninstall-all
        # elif args.uninstall_all: # Example hypothetical argument
        #    log.warning("Executing full uninstallation via command line...")
        #    success = uninstaller.uninstall_everything()
        #    return 0 if success else 1

        # If no specific action args, run the interactive menu
        return run_menu(uninstaller)

    except KeyboardInterrupt:
        print() # Ensure newline after ^C
        log.warning("Operation cancelled by user (Ctrl+C).")
        return 1 # Indicate cancellation
    except Exception as e:
        print() # Ensure newline before error
        log.critical("An unexpected critical error occurred", e)
        log.critical("Please report this issue with the logs.")
        return 1 # Indicate error


if __name__ == "__main__":
    sys.exit(main())
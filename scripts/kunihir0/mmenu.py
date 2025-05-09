#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kunihir0 Main Menu Script
Provides a central menu to launch various utilities.
"""

import subprocess
import sys
from pathlib import Path

try:
    # Adjust path for relative imports when run as part of the package
    from .utils.theme_manager import get_theme_manager, ThemeConfig
except ImportError:
    # Fallback for direct execution (e.g., for development/testing)
    # This assumes 'scripts' is in PYTHONPATH or the script is run from project root.
    # You might need to adjust this based on your project structure and how you run scripts.
    sys.path.append(str(Path(__file__).resolve().parents[2])) # Add project root to path
    from scripts.kunihir0.utils.theme_manager import get_theme_manager, ThemeConfig


def main():
    """
    Main function to display and handle the menu.
    """
    try:
        theme_manager = get_theme_manager()
        theme_manager.config.set_theme(ThemeConfig.THEME_STANDARD)
    except Exception as e:
        print(f"Error initializing theme manager: {e}", file=sys.stderr)
        sys.exit(1)

    title = "Kunihir0 Main Menu"
    subheading = "A conductor to launch various Kunihir0 scripts and utilities"
    options = [
        {"title": "Cleanup Utility", "description": "Launch the ULTMOS cleanup and uninstaller tool"},
        {"title": "Exit", "description": "Exit the main menu"}
    ]

    # Determine the base path for scripts relative to this file
    # mmenu.py is in scripts/kunihir0/
    # cleanup.py is in scripts/kunihir0/cleanup/cleanup.py
    base_script_path = Path(__file__).resolve().parent

    try:
        while True:
            theme_manager.display_menu(title=title, subheading=subheading, options=options)
            choice = theme_manager.get_user_choice()

            if not choice: # User might have cancelled or entered invalid input handled by theme_manager
                theme_manager.display_step("No valid option selected or operation cancelled. Please try again.", "warning")
                continue

            # Assuming get_user_choice returns the 1-based index as a string or the selected option's title
            # For simplicity, let's assume it returns the title if it's a dictionary based selection,
            # or the string index if it's a simple list.
            # The example implies choice "1", "2", so we'll map based on option index.

            selected_option_title = ""
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                selected_option_title = options[int(choice) - 1]["title"]
            elif choice in [opt["title"] for opt in options]: # If get_user_choice returns the title
                 selected_option_title = choice
            else:
                theme_manager.display_step(f"Invalid choice: {choice}. Please select a valid option number.", "error")
                continue


            if selected_option_title == "Cleanup Utility":
                cleanup_script_module_name = "scripts.kunihir0.cleanup.cleanup"
                # For display purposes, we can still show the nominal path
                cleanup_script_display_path = base_script_path / "cleanup" / "cleanup.py"
                project_root = Path(__file__).resolve().parents[2]

                theme_manager.display_step(f"Launching Cleanup Utility module: {cleanup_script_module_name} (from {cleanup_script_display_path})...", "info")
                try:
                    # Run the cleanup utility module, allowing it to interact with the terminal directly
                    process_result = subprocess.run(
                        [sys.executable, "-m", cleanup_script_module_name],
                        check=True, # Still check for errors
                        # capture_output=False, # Default, no need to specify
                        # text=False, # Default, no need to specify
                        cwd=project_root  # Run from the project root
                    )
                    theme_manager.display_step("Cleanup Utility finished.", "info_highlight")
                    # Output is no longer captured, so these checks are removed
                    # if process_result.stdout:
                    #     print("\nCleanup Utility Output:\n" + "="*25 + "\n" + process_result.stdout)
                    # if process_result.stderr:
                    #     print("\nCleanup Utility Errors:\n" + "="*25 + "\n" + process_result.stderr)

                except FileNotFoundError: # This would typically be if sys.executable is not found
                    theme_manager.display_step(f"Error: Python interpreter ({sys.executable}) not found or module path incorrect.", "error")
                except subprocess.CalledProcessError as e:
                    theme_manager.display_step(f"Error running Cleanup Utility: Process returned code {e.returncode}", "error")
                    # Output is no longer captured, so these checks are removed
                    # if e.stdout:
                    #     print("\nCleanup Utility Output (on error):\n" + "="*35 + "\n" + e.stdout)
                    # if e.stderr:
                    #     print("\nCleanup Utility Errors (on error):\n" + "="*35 + "\n" + e.stderr)
                except Exception as e:
                    theme_manager.display_step(f"An unexpected error occurred while launching Cleanup Utility: {e}", "error")
                
                theme_manager.display_step("Press Enter to return to the main menu...", "info")
                input() # Wait for user to acknowledge before re-displaying menu

            elif selected_option_title == "Exit":
                theme_manager.display_step("Exiting Kunihir0 Main Menu...", "info")
                sys.exit(0)
            else:
                # This case should ideally be caught by the initial choice validation
                theme_manager.display_step(f"Unrecognized option: {selected_option_title}. Please try again.", "warning")
    except KeyboardInterrupt:
        print() # Newline after ^C
        theme_manager.display_step("Exiting Kunihir0 Main Menu due to user interruption...", "info")
        sys.exit(0)
    except Exception as e:
        print() # Newline
        theme_manager.display_step(f"An unexpected error occurred in the main menu: {e}", "error")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ULTMOS Safe Uninstaller Theme Manager.

This module serves as a conductor between different UI themes for the ULTMOS
Safe Uninstaller, allowing for seamless switching between the standard ULTMOS TUI
and the custom animated theme while maintaining compatibility.
"""

# --- Standard Library Imports ---
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Callable

# --- Add Project Root to sys.path ---
try:
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[3]  # Navigate up from scripts/kunihir0/utils/ to project root
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except IndexError:
    print("Error: Could not determine project root. Ensure script is run from within the project structure.", file=sys.stderr)
    sys.exit(1)

# --- Define Standard TUI Module locally ---
# Instead of importing from scripts.extras which causes circular imports,
# we'll define the necessary components here
class cpyd_tui:
    class cpyd:
        HEADING = "ULTMOS SAFE UNINSTALLER"
        SUBHEADING = "Safely remove ULTMOS components"
        BODY_1 = "This utility helps you safely remove ULTMOS components from your system."
        BODY_2 = "You can remove VMs, clean temporary files, or uninstall everything."
        BODY_3 = "Use with caution - some operations cannot be undone."
        BODY_4 = "Backup your important data before proceeding."
        CALLTOACTION = "SELECT AN OPTION:"
        USER_SELECT_TITLE_1 = "REMOVE VMS ONLY"
        USER_SELECT_TITLE_2 = "CLEAN TEMPORARY FILES"
        USER_HELP_TITLE = "HELP"
        USER_ESCAPE_TITLE = "EXIT"
        INPUT_FIELD_TEXT = "Select"

    @staticmethod
    def startup():
        pass

class cpyd_color:
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    END = "\033[0m"

try:
    sys.path.append('./resources/python')
    from cpydColours import color as cpyd_color_ext
    # Use imported colors if available
    if hasattr(cpyd_color_ext, 'BOLD'):
        cpyd_color = cpyd_color_ext
except ImportError:
    # Already defined fallback above
    pass

# --- Custom theme imports ---
# Import all necessary components from safe_visual_utils at the top
from .safe_visual_utils import TerminalDisplay, TerminalColor, ProgressDisplay

# --- Theme Configuration ---
class ThemeConfig:
    """Configuration class for the Theme Manager."""
    
    THEME_STANDARD = "standard"
    THEME_ANIMATED = "animated"
    
    def __init__(self):
        """Initialize with default theme settings."""
        self.current_theme = self.THEME_STANDARD
        self.self_destruct_quiet_mode = False
        
    def toggle_theme(self) -> str:
        """Toggle between standard and animated themes."""
        if self.current_theme == self.THEME_STANDARD:
            self.current_theme = self.THEME_ANIMATED
        else:
            self.current_theme = self.THEME_STANDARD
        return self.current_theme
        
    def set_theme(self, theme: str) -> None:
        """Set the theme explicitly."""
        if theme in [self.THEME_STANDARD, self.THEME_ANIMATED]:
            self.current_theme = theme
            
    def toggle_quiet_mode(self) -> bool:
        """Toggle between quiet and full animation modes for self-destruct."""
        self.self_destruct_quiet_mode = not self.self_destruct_quiet_mode
        return self.self_destruct_quiet_mode

# --- Global instance ---
theme_config = ThemeConfig()

# --- Standard Theme Implementation ---
class StandardTheme:
    """Implementation of the standard ULTMOS TUI theme."""
    
    def __init__(self):
        """Initialize with the cpyd_tui styles and colors."""
        self.cpyd = cpyd_tui.cpyd
        self.color = cpyd_color
        
    def display_menu(self, title: str = None, subheading: str = None, 
                    body_lines: list = None, options: list = None) -> None:
        """Display a menu in the standard ULTMOS TUI style."""
        # Use provided content or defaults from cpyd_tui
        self.cpyd.HEADING = title or self.cpyd.HEADING
        self.cpyd.SUBHEADING = subheading or self.cpyd.SUBHEADING
        
        if body_lines and len(body_lines) >= 4:
            self.cpyd.BODY_1 = body_lines[0]
            self.cpyd.BODY_2 = body_lines[1]
            self.cpyd.BODY_3 = body_lines[2]
            self.cpyd.BODY_4 = body_lines[3]
            
        # Clear the screen
        print("\n" * 2)
        
        # Print the header
        print("\n\n  "+self.color.BOLD+self.color.GREEN, self.cpyd.HEADING+self.color.END, "")
        print("  ", self.cpyd.SUBHEADING+self.color.END+"\n")
        
        # Print body text
        print("  ", self.cpyd.BODY_1, "\n  ", self.cpyd.BODY_2, "\n  ", 
              self.cpyd.BODY_3, "\n  ", self.cpyd.BODY_4, "\n  "+self.color.END)
        
        # Print call to action
        print("  ", self.cpyd.CALLTOACTION)
        
        # Print options
        # TerminalColor is now imported at the top of the module

        if options:
            for i, option in enumerate(options):
                option_num_title = f"{str(i+1)}. {option['title']}"
                
                # Use the color specified in the option, fallback to BOLD if no color or not supported
                # TerminalColor.colorize handles the supports_color check internally.
                # Ensure option.get("color") is passed to colorize. If it's None, colorize handles it.
                colored_title = TerminalColor.colorize(option_num_title, option.get("color"))
                
                # If no color was specified in the option dict, and thus colorize might have returned plain text,
                # and we want a default bold style.
                # TerminalColor.colorize itself will apply "bold" style if "bold" string is passed.
                # If option.get("color") is None, colorize returns plain text.
                # We want to ensure that if no color is specified, it defaults to bold.
                if not option.get("color"): # If no color was specified, make it bold by default
                    title_to_print = f"{self.color.BOLD}{option_num_title}{self.color.END}"
                else:
                    # Use the already colorized title (which might include bold if "bold" was the color)
                    title_to_print = colored_title
                
                print("\n      " + title_to_print)
                
                description = option.get("description")
                if description:
                    # Indent description. cpyd-tui example uses 8 spaces.
                    # Descriptions are kept plain (default terminal color) for readability in standard theme.
                    print("        ", description)
                    
        print()  # Extra spacing
        
    def get_user_choice(self, prompt: str = None) -> str:
        """Get user input with the standard prompt style."""
        input_prompt = prompt or self.cpyd.INPUT_FIELD_TEXT
        choice = input(self.color.BOLD + input_prompt + "> " + self.color.END)
        return choice
        
    def display_step(self, message: str, status: str = "") -> None:
        """Display a step message in standard style."""
        prefix = ""
        if status == "info":
            prefix = "INFO: "
        elif status == "warning":
            prefix = "WARNING: "
        elif status == "error":
            prefix = "ERROR: "
        elif status == "success":
            prefix = "SUCCESS: "
            
        print(f"  {prefix}{message}")
        
    def display_progress(self, message: str, progress: float = 0.0) -> None:
        """Display a simple progress bar in standard style."""
        bar_width = 30
        filled_width = int(bar_width * progress)
        bar = "#" * filled_width + "-" * (bar_width - filled_width)
        percent = int(progress * 100)
        print(f"\r  {message}: [{bar}] {percent}%", end="", flush=True)
        
    def clear_screen(self) -> None:
        """Clear the screen in standard way."""
        print("\n" * 150)  # Simple screen clearing
        
    def print_banner(self, title: str) -> None:
        """Print a simple banner with the title."""
        print("\n\n  " + self.color.BOLD + self.color.GREEN + title + self.color.END + "\n")

# --- Animated Theme Implementation ---
class AnimatedTheme:
    """Implementation of the custom animated theme."""
    
    def __init__(self):
        """Initialize with TerminalDisplay style."""
        pass
        
    def display_menu(self, title: str = None, subheading: str = None, 
                    body_lines: list = None, options: list = None) -> None:
        """Display a menu with animations and styling."""
        # Clear screen first
        TerminalDisplay.clear_screen()
        
        # Display title banner
        TerminalDisplay.print_banner(title or "ULTMOS Safe Uninstaller")
        
        if subheading:
            TerminalDisplay.print_centered(subheading, "bright_cyan")
            
        # Display body lines with spacing
        if body_lines:
            print() # Single newline before body
            for line in body_lines:
                TerminalDisplay.print_centered(line, color="bright_black") # Use bright_black for a dim effect
            print() # Single newline after body
        
        # Display menu options with colors
        if options:
            for i, option in enumerate(options):
                if "color" in option:
                    TerminalDisplay.print_centered(f"{i+1}. {option['title']}", option["color"])
                else:
                    # Alternate colors for visual distinction
                    colors = ["bright_cyan", "bright_yellow", "bright_magenta", 
                             "bright_blue", "bright_green", "bright_red"]
                    color = colors[i % len(colors)]
                    TerminalDisplay.print_centered(f"{i+1}. {option['title']}", color)
                
                description = option.get("description")
                if description:
                    # Center description, use bright_black for dim effect, allow override with color_subtext
                    desc_color = option.get("color_subtext", "bright_black")
                    TerminalDisplay.print_centered(description, color=desc_color)
                    print() # Add a bit of space after description
                    
        print("\n")  # Extra spacing
        
    def get_user_choice(self, prompt: str = None) -> str:
        """Get user input with animated prompt style."""
        # TerminalColor is now imported at the top of the module
        choice = input(TerminalColor.colorize(prompt or "Select option> ", "bold"))
        return choice
        
    def display_step(self, message: str, status: str = "") -> None:
        """Display a step message with animation and color."""
        TerminalDisplay.print_step(message, status)
        
    def display_progress(self, message: str, progress: float = 0.0) -> None:
        """Display an animated progress bar."""
        # ProgressDisplay is now imported at the top of the module
        ProgressDisplay.progress_bar(progress, message)
        
    def clear_screen(self) -> None:
        """Clear the screen with animation."""
        TerminalDisplay.clear_screen()
        
    def print_banner(self, title: str) -> None:
        """Print an animated banner with the title."""
        TerminalDisplay.print_banner(title)

# --- Theme Manager Implementation ---
class ThemeManager:
    """Main theme manager class that coordinates between different themes."""
    
    def __init__(self):
        """Initialize the theme manager with both theme implementations."""
        self.config = theme_config
        self.standard_theme = StandardTheme()
        self.animated_theme = AnimatedTheme()
        
    @property
    def current_theme(self):
        """Get the current active theme implementation."""
        if self.config.current_theme == ThemeConfig.THEME_STANDARD:
            return self.standard_theme
        else:
            return self.animated_theme
            
    def display_menu(self, title: str = None, subheading: str = None, 
                    body_lines: list = None, options: list = None) -> None:
        """Display a menu using the current theme."""
        self.current_theme.display_menu(title, subheading, body_lines, options)
        
    def get_user_choice(self, prompt: str = None) -> str:
        """Get user input using the current theme."""
        return self.current_theme.get_user_choice(prompt)
        
    def display_step(self, message: str, status: str = "") -> None:
        """Display a step message using the current theme."""
        self.current_theme.display_step(message, status)
        
    def display_progress(self, message: str, progress: float = 0.0) -> None:
        """Display a progress bar using the current theme."""
        self.current_theme.display_progress(message, progress)
        
    def clear_screen(self) -> None:
        """Clear the screen using the current theme."""
        self.current_theme.clear_screen()
        
    def print_banner(self, title: str) -> None:
        """Print a banner using the current theme."""
        self.current_theme.print_banner(title)
        
    def toggle_theme(self) -> str:
        """Toggle between themes and return the new theme name."""
        return self.config.toggle_theme()
        
    def get_theme_name(self) -> str:
        """Get the name of the current theme."""
        return self.config.current_theme
        
    def get_theme_display_name(self) -> str:
        """Get a user-friendly display name for the current theme."""
        if self.config.current_theme == ThemeConfig.THEME_STANDARD:
            return "STANDARD"
        else:
            return "ANIMATED"
            
    def is_quiet_mode(self) -> bool:
        """Check if quiet mode is enabled for self-destruct operations."""
        return self.config.self_destruct_quiet_mode
        
    def toggle_quiet_mode(self) -> bool:
        """Toggle quiet mode for self-destruct operations."""
        return self.config.toggle_quiet_mode()

# Create a global instance of the theme manager
theme_manager = ThemeManager()

# Helper function to get the current theme manager instance
def get_theme_manager() -> ThemeManager:
    """Get the global instance of the theme manager."""
    return theme_manager

if __name__ == "__main__":
    # Simple test for the theme manager
    tm = get_theme_manager()
    
    # Test standard theme
    print("Testing Standard Theme:")
    options = [
        {"title": "OPTION ONE", "description": "This is the first option"},
        {"title": "OPTION TWO", "description": "This is the second option"},
        {"title": "HELP", "description": "Get help"},
        {"title": "EXIT", "description": "Exit the application"}
    ]
    tm.display_menu("TEST MENU", "Test Subheading", 
                   ["Line 1", "Line 2", "Line 3", "Line 4"], options)
    
    # Toggle to animated theme
    tm.toggle_theme()
    print("\n\nTesting Animated Theme:")
    tm.display_menu("TEST MENU", "Test Subheading", 
                   ["Line 1", "Line 2", "Line 3", "Line 4"], options)
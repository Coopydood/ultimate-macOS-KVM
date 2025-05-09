#!/usr/bin/env python3

"""
Safe visual utilities for terminal display in the ULTMOS uninstaller.

This module provides a platform-independent approach to terminal interfaces
while following the ULTMOS coding standards:
- Uses platform-independent approaches instead of direct ANSI codes
- Follows type safety principles with proper annotations
- Provides proper error handling
- Relies on the centralized logging system
"""

import sys
import time
import shutil
import platform
import subprocess
# Removed os import to comply with coding standards
from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple, Any, Callable

# Import the centralized logger
from .logger import default_logger as log


class TerminalColor:
    """
    Terminal color codes with platform-independent usage.
    
    This class provides a platform-independent way to use colors in the terminal
    while following the coding standards.
    """
    
    # Define standard ANSI color codes but abstract their usage
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Use for mapping symbolic names to codes
    _color_map = {
        "reset": RESET,
        "bold": BOLD,
        "underline": UNDERLINE,
        "black": BLACK,
        "red": RED,
        "green": GREEN,
        "yellow": YELLOW,
        "blue": BLUE,
        "magenta": MAGENTA,
        "cyan": CYAN,
        "white": WHITE,
        "bright_black": BRIGHT_BLACK,
        "bright_red": BRIGHT_RED,
        "bright_green": BRIGHT_GREEN,
        "bright_yellow": BRIGHT_YELLOW,
        "bright_blue": BRIGHT_BLUE,
        "bright_magenta": BRIGHT_MAGENTA,
        "bright_cyan": BRIGHT_CYAN,
        "bright_white": BRIGHT_WHITE
    }
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """
        Apply a color to text in a platform-independent way.
        
        Args:
            text: The text to colorize
            color: Color name (e.g., "red", "bright_green", "default")
            
        Returns:
            Colorized text string
        """
        if color is None:
            return text # No color to apply, return original text

        normalized_color = color.lower()
        if normalized_color == "default":
            # "default" color means no specific ANSI color code, effectively resetting to terminal default.
            # The final cls.RESET in the standard path handles resetting after colored text.
            # For "default", we return the text as is, without adding color codes or warnings.
            return text

        color_code = cls._color_map.get(normalized_color, "")
        if not color_code:
            log.warning(f"Unknown color: {color}")
            return text # Return original text if color is unknown
            
        return f"{color_code}{text}{cls.RESET}"
    
    @classmethod
    def supports_color(cls) -> bool:
        """
        Check if the current terminal supports color output (Linux focused).

        Returns:
            True if color is supported (stdout is a TTY).
        """
        # For Linux, the primary check is if stdout is a TTY.
        # No need for os.environ or platform checks per user feedback.
        is_tty = sys.stdout.isatty()
        log.debug(f"Terminal supports color (is TTY): {is_tty}")
        return is_tty


class TerminalDisplay:
    """
    Platform-independent terminal display utilities.
    
    This class provides methods for manipulating the terminal display
    in a platform-independent way.
    """
    
    @staticmethod
    def clear_screen() -> None:
        """
        Clear the terminal screen in a platform-independent way.
        """
        try:
            # Determine which command to use based on platform
            system = platform.system()
            if system == "Windows":
                subprocess.run(["cls"], shell=True, check=False)
            else:
                subprocess.run(["clear"], check=False)
        except Exception as e:
            # Fallback method if subprocess fails
            log.warning(f"Error clearing screen with subprocess: {e}")
            print("\n" * 100)  # Simple fallback: print many newlines
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """
        Get terminal dimensions in a platform-independent way.
        
        Returns:
            Tuple of (columns, rows)
        """
        try:
            columns, rows = shutil.get_terminal_size()
            return columns, rows
        except Exception as e:
            log.debug(f"Error getting terminal size: {e}")
            return 80, 24  # Default fallback size
    
    @classmethod
    def print_centered(cls, text: str, color: Optional[str] = None) -> None:
        """
        Print text centered in the terminal.
        
        Args:
            text: Text to center and print
            color: Optional color name (e.g., "red", "bright_blue")
        """
        columns, _ = cls.get_terminal_size()
        padding = max(0, (columns - len(text)) // 2)
        
        output_text = " " * padding + text
        if color and TerminalColor.supports_color():
            output_text = TerminalColor.colorize(output_text, color)
            
        print(output_text)
    
    @classmethod
    def print_banner(cls, title: str, subtitle: Optional[str] = None) -> None:
        """
        Print a styled banner with borders.
        
        Args:
            title: Main banner title
            subtitle: Optional subtitle
        """
        cls.clear_screen()
        columns, _ = cls.get_terminal_size()
        
        # Calculate banner width based on terminal width
        banner_width = min(columns - 8, 60)
        
        print("\n")
        cls.print_centered("╭" + "─" * banner_width + "╮", "bright_red")
        print("\n")
        cls.print_centered(title.upper(), "bright_red")
        
        if subtitle:
            cls.print_centered(subtitle, "bright_red")
            
        print("\n")
        cls.print_centered("╰" + "─" * banner_width + "╯", "bright_red")
        print("\n")
    
    @classmethod
    def print_step(cls, step: str, status: Optional[str] = None) -> None:
        """
        Print a step with optional status indicator.
        
        Args:
            step: Step description
            status: Status indicator ('success', 'fail', 'warning', 'info')
        """
        status_symbol = ""
        color = None
        
        if status == "success":
            status_symbol = "✓"
            color = "bright_green"
        elif status == "fail":
            status_symbol = "✗"
            color = "bright_red"
        elif status == "warning":
            status_symbol = "⚠"
            color = "bright_yellow"
        elif status == "info":
            # status_symbol = "ℹ" # Remove symbol for info status
            color = "bright_blue" # Keep the color
            
        display_text = step
        if status_symbol:
            display_text = f"{step} {status_symbol}"
            
        cls.print_centered(display_text, color)


class ProgressDisplay:
    """
    Progress display utilities.
    
    This class provides methods for displaying progress indicators
    in a platform-independent way.
    """
    
    # Unicode characters for visual elements
    BLOCK_FULL = "█"
    BLOCK_LIGHT = "░"
    SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    @classmethod
    def progress_bar(
        cls, 
        progress: float, 
        label: str = "", 
        width: int = 40,
        clear_after: bool = False
    ) -> None:
        """
        Display a progress bar.
        
        Args:
            progress: Progress value from 0.0 to 1.0
            label: Text to display next to the progress bar
            width: Width of the progress bar in characters
            clear_after: Whether to clear the line after completing
        """
        columns, _ = TerminalDisplay.get_terminal_size()
        bar_width = min(width, columns - 20)
        
        # Ensure progress is within [0, 1]
        progress = max(0.0, min(1.0, progress))
        
        filled_length = int(bar_width * progress)
        bar = cls.BLOCK_FULL * filled_length + cls.BLOCK_LIGHT * (bar_width - filled_length)
        percent = int(100 * progress)
        
        # Center the progress bar
        padding = max(0, (columns - (bar_width + 10 + len(label))) // 2)
        
        sys.stdout.write("\r" + " " * padding + f"{label} [{bar}] {percent}%")
        sys.stdout.flush()
        
        if progress >= 1 or clear_after:
            sys.stdout.write("\n")
    
    @classmethod
    def spinner(cls, text: str, seconds: float = 0.1, quiet: bool = False) -> None:
        """
        Display an animated spinner with text.
        
        Args:
            text: Text to display next to spinner
            seconds: Time to show spinner animation (in seconds)
            quiet: If True, don't display spinner (for non-interactive use)
        """
        if quiet or not sys.stdout.isatty():
            # In quiet mode or non-interactive terminal, just log the message
            log.info(text)
            time.sleep(seconds)
            return
            
        start_time = time.time()
        i = 0
        
        while time.time() - start_time < seconds:
            spinner_char = cls.SPINNER_CHARS[i % len(cls.SPINNER_CHARS)]
            colored_spinner = TerminalColor.colorize(spinner_char, "bright_cyan")
            sys.stdout.write(f"\r{colored_spinner} {text}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
            
        # Clear the spinner line
        sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
        sys.stdout.flush()


def display_operation(
    operation: str, 
    steps: List[Callable[[], Any]], 
    labels: Optional[List[str]] = None
) -> bool:
    """
    Display an operation with progress.
    
    Args:
        operation: Name of the operation
        steps: List of step functions to execute
        labels: Optional labels for each step
        
    Returns:
        True if all steps succeeded, False otherwise
    """
    if labels is None:
        labels = [f"Step {i+1}/{len(steps)}" for i in range(len(steps))]
    
    TerminalDisplay.print_step(f"{operation} - Starting", "info")
    
    success = True
    for i, (step, label) in enumerate(zip(steps, labels)):
        ProgressDisplay.spinner(label, 0.2)
        
        try:
            step()
            ProgressDisplay.progress_bar((i + 1) / len(steps), operation, 30)
        except Exception as e:
            log.error(f"Error in {label}", e)
            success = False
            break
    
    if success:
        TerminalDisplay.print_step(f"{operation} - Completed", "success")
    else:
        TerminalDisplay.print_step(f"{operation} - Failed", "fail")
        
    return success
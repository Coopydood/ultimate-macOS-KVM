#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --- ULTMOS Self-Destruct Script ---
# This script is copied to a temporary location and run detached with sudo.
# It performs final cleanup actions after the main process exits.
# It is designed to be dependency-free, using only standard Python libraries.

import sys
import time
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple
import math
import random
import os
from collections import deque

# --- Visual Mode Control ---
VISUAL_MODE = "full" # "full" or "minimal"

# --- Enhanced Visual Feedback Functions (Dependency-Free) ---
SPINNER_CHARS = ["✿", "❀", "✾", "❁", "✽", "✼", "✻", "✺", "✹", "✸"]
COLORS = {
    "reset": "\033[0m",
    "pink": "\033[38;5;219m",
    "purple": "\033[38;5;183m",
    "cyan": "\033[38;5;123m",
    "yellow": "\033[38;5;228m",
    "orange": "\033[38;5;216m",
    "green": "\033[38;5;156m",
    "red": "\033[38;5;210m",
    "blue": "\033[38;5;111m",
    "magenta": "\033[38;5;201m",
    "light_blue": "\033[38;5;159m",
    "lavender": "\033[38;5;147m",
    "peach": "\033[38;5;223m",
    "mint": "\033[38;5;121m",
    "bold": "\033[1m",
    "bg_black": "\033[40m",
    "bg_purple": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_pink": "\033[48;5;219m",
    "bg_dark": "\033[48;5;236m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "blink": "\033[5m"
}

# ASCII Art for intro - more playful style
ULTMOS_LOGO = """
 ╭─────────────────────────────────────╮
 │                                     │
 │  ✨  U L T M O S  ✨                │
 │   _   _  _   _____ __  __  ___  ___ │
 │  | | | || | |_   _|  \\/  |/ _ \\/ __││
 │  | | | || |   | | | |\\/| | | | \\__ \\│
 │  | |_| || |___| | | |  | | |_| |___)│
 │   \\___/ |_____|_| |_|  |_|\\___/|____│
 │                                     │
 │      ✧ cleanup & uninstall ✧       │
 │                                     │
 ╰─────────────────────────────────────╯
"""

# Smaller version for when screen space is needed
SMALL_LOGO = """
 ✨ ULTMOS CLEANUP ✨ 
"""

# Terminal control sequences
def _clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def _get_terminal_size() -> Tuple[int, int]:
    """Get terminal width and height."""
    try:
        columns, rows = os.get_terminal_size(0)
        return columns, rows
    except (OSError, AttributeError):
        return 80, 24  # Default fallback size

def _move_cursor(x, y):
    """Move cursor to position x, y."""
    print(f"\033[{y};{x}H", end="", flush=True)

def _save_cursor_position():
    """Save the current cursor position."""
    print("\033[s", end="", flush=True)

def _restore_cursor_position():
    """Restore the saved cursor position."""
    print("\033[u", end="", flush=True)

def _hide_cursor():
    """Hide the terminal cursor."""
    print("\033[?25l", end="", flush=True)

def _show_cursor():
    """Show the terminal cursor."""
    print("\033[?25h", end="", flush=True)

def _color_text(text, color="reset", bg_color=None, styles=None):
    """Add color and styles to terminal text."""
    result = ""
    if bg_color:
        bg_key = f"bg_{bg_color}"
        if bg_key in COLORS:
            result += COLORS[bg_key]
    
    if color in COLORS:
        result += COLORS[color]
    
    if styles:
        for style in styles:
            if style in COLORS:
                result += COLORS[style]
    
    result += text + COLORS["reset"]
    return result

def _center_text(text, width=None, padding_char=" "):
    """Center text in the given width or terminal width."""
    if width is None:
        width, _ = _get_terminal_size()
    # Calculate length considering ANSI escape codes might be present
    plain_text_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout)
    padding = (width - plain_text_len) // 2
    if padding < 0:
        padding = 0
    return padding_char * padding + text

def _gradient_text(text, colors=None):
    """Create a color gradient across text."""
    global VISUAL_MODE
    if colors is None:
        colors = ["pink", "purple", "cyan", "blue", "magenta"]
   
    if VISUAL_MODE == "minimal":
        # Minimal mode: use the first color or a default
        default_color = colors[0] if colors else "cyan"
        return _color_text(text, default_color)

    # Calculate color positions
    gradient = []
    for i in range(len(text)):
        color_idx = int((i / len(text)) * len(colors))
        if color_idx >= len(colors):
            color_idx = len(colors) - 1
        gradient.append(COLORS[colors[color_idx]] + text[i])
    
    # Add reset at the end
    return "".join(gradient) + COLORS["reset"]

def _animate_text_reveal(text, delay=0.02, color=None, gradient=False, center=False, rainbow=False, minimal_direct_print=False):
    """Reveal text character by character with optional color."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal" or minimal_direct_print:
        effective_delay = 0.001 # Typewriter effect for minimal
    else:
        effective_delay = delay

    width, _ = _get_terminal_size()
    
    if center:
        # Calculate length considering ANSI escape codes might be present
        plain_text_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout)
        padding = (width - plain_text_len) // 2
        if padding < 0:
            padding = 0
        sys.stdout.write(" " * padding)
    
    if rainbow:
        rainbow_colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]
        color_idx = 0
        for char in text:
            sys.stdout.write(f"{COLORS[rainbow_colors[color_idx % len(rainbow_colors)]]}{char}{COLORS['reset']}")
            sys.stdout.flush()
            time.sleep(effective_delay)
            color_idx += 1
    elif gradient:
        gradient_colors = ["pink", "purple", "cyan", "blue", "magenta"] if gradient is True else gradient
        for i, char in enumerate(text):
            color_idx = int((i / len(text)) * len(gradient_colors))
            if color_idx >= len(gradient_colors):
                color_idx = len(gradient_colors) - 1
            sys.stdout.write(f"{COLORS[gradient_colors[color_idx]]}{char}{COLORS['reset']}")
            sys.stdout.flush()
            time.sleep(effective_delay)
    elif color:
        for char in text:
            sys.stdout.write(f"{COLORS[color]}{char}{COLORS['reset']}")
            sys.stdout.flush()
            time.sleep(effective_delay)
    else:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(effective_delay)
    print()

def _sparkle_effect(text, duration=1.5, density=3, colors=None):
    """Create a sparkle effect across the text."""
    global VISUAL_MODE
    if colors is None:
        colors = ["pink", "purple", "cyan", "yellow", "green", "blue"]

    if VISUAL_MODE == "minimal":
        # _clear_screen() # Removed for verbosity
        print(_center_text(_gradient_text(text, colors)), flush=True) # Gradient will be simplified by _gradient_text
        time.sleep(0.1) # Brief pause
        return
    # colors is already handled by the check at the beginning of the function if VISUAL_MODE is "full"
        
    sparkles = ["✨", "✧", "✦", "⋆", "✩", "✫", "✬", "✭", "✮", "✯", "★", "*"]
    width, height = _get_terminal_size()
    # Calculate length considering ANSI escape codes might be present
    plain_text_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout)
    padding = (width - plain_text_len) // 2
    
    # Create a blank canvas
    canvas = [[" " for _ in range(width)] for _ in range(height)]
    
    # Calculate text position (centered)
    text_row = height // 2
    text_start = padding
    
    # Print the initial state
    _hide_cursor()
    _clear_screen()
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Add sparkles
        for _ in range(density):
            # Generate random positions with higher density near the text
            if random.random() < 0.7:  # 70% chance to place sparkle near text
                x = random.randint(max(0, text_start - 5), min(width - 1, text_start + plain_text_len + 5))
                y_spread = int(height * 0.4)  # Concentrate within 40% of screen height
                y = random.randint(max(0, text_row - y_spread), min(height - 1, text_row + y_spread))
            else:  # 30% chance for totally random position
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
            
            # Check if we're not overwriting text
            if y == text_row and text_start <= x < text_start + plain_text_len:
                continue
                
            # Add sparkle with random color
            color = random.choice(colors)
            sparkle = random.choice(sparkles)
            canvas[y][x] = f"{COLORS[color]}{sparkle}{COLORS['reset']}"
        
        # Now draw the canvas
        _move_cursor(1, 1)
        
        for y in range(height):
            for x in range(width):
                # Draw the text at its position
                if y == text_row and text_start <= x < text_start + plain_text_len:
                    char_idx = x - text_start
                    # Apply gradient to text
                    color_idx = int((char_idx / plain_text_len) * len(colors))
                    if color_idx >= len(colors):
                        color_idx = len(colors) - 1
                    # Need to handle the actual characters of the input text, not just index
                    # This requires a way to access the plain text characters
                    # For simplicity, let's assume text is plain for this effect or use a placeholder
                    # A more robust solution would parse the plain text first.
                    # Using placeholder 'T' for now.
                    # TODO: Improve this to handle actual text characters if needed.
                    current_char = text[char_idx] if char_idx < len(text) else ' ' # Basic handling
                    print(f"{COLORS[colors[color_idx]]}{current_char}{COLORS['reset']}", end="")
                else:
                    # Draw the sparkle canvas
                    print(canvas[y][x], end="")
            print()
            
        # Fade some sparkles
        for y in range(height):
            for x in range(width):
                if canvas[y][x] != " " and random.random() < 0.3:  # 30% chance to fade
                    canvas[y][x] = " "
        
        time.sleep(0.08)
    
    # Clean up
    _clear_screen()
    _show_cursor()
    # Print the final text centered
    print(_center_text(_gradient_text(text, colors)), flush=True)

def _bubble_effect(text, duration=1.0, speed=0.08):
    """Create bubbling text effect."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        print(_center_text(_color_text(text, "cyan")), flush=True) # Simple colored text
        time.sleep(0.1)
        return
    bubbles = ["○", "◌", "◍", "◎", "●", "◉"]
    bubble_colors = ["pink", "purple", "cyan", "yellow", "light_blue", "lavender"]
    
    # Initial display
    _hide_cursor()
    width, _ = _get_terminal_size()
    # Calculate length considering ANSI escape codes might be present
    plain_text_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout)
    padding = (width - plain_text_len) // 2
    
    start_time = time.time()
    bubbling_chars = set()
    
    while time.time() - start_time < duration:
        # Clear line
        print("\r" + " " * width, end="\r")
        
        # Generate new bubbling characters
        if random.random() < 0.3:  # 30% chance to add a new bubbling character
            if len(bubbling_chars) < plain_text_len // 2:  # Limit number of active bubbles
                bubbling_chars.add(random.randint(0, plain_text_len - 1))
        
        # Generate the display
        display = " " * padding
        # Need to iterate through plain text characters for indexing
        # Assuming text is plain for simplicity here
        # TODO: Improve this to handle ANSI codes if needed
        plain_text = subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout
        for i, char in enumerate(plain_text):
            if i in bubbling_chars:
                bubble = random.choice(bubbles)
                color = random.choice(bubble_colors)
                display += f"{COLORS[color]}{bubble}{COLORS['reset']}"
                
                # Remove from bubbling set with some probability
                if random.random() < 0.2:  # 20% chance to stop bubbling
                    bubbling_chars.discard(i) # Use discard to avoid errors if already removed
            else:
                display += char
                
        sys.stdout.write(display)
        sys.stdout.flush()
        time.sleep(speed)
    
    # Final display is the clean text
    print("\r" + " " * width, end="\r")
    print(_center_text(text), flush=True)
    _show_cursor()

def _wave_text(text, cycles=1, speed=0.002, amplitude=3, rainbow=False):
    """Create a sine wave animation of text."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        # _clear_screen() # Removed for verbosity
        if rainbow:
            colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]
            color_text_minimal = ""
            for i, char in enumerate(text):
                color_idx = i % len(colors)
                color_text_minimal += f"{COLORS[colors[color_idx]]}{char}{COLORS['reset']}"
            print(_center_text(color_text_minimal))
        else:
            print(_center_text(_color_text(text, "cyan"))) # Default color
        time.sleep(0.1)
        return

    width, height = _get_terminal_size()
    # Calculate length considering ANSI escape codes might be present
    plain_text_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout)
    
    # Ensure text fits in terminal
    if plain_text_len > width - 4:
        # Truncation needs to happen carefully if text has ANSI codes
        # For simplicity, assume plain text or accept potential display issues
        text = text[:width-4] # Basic truncation
        plain_text_len = len(text)
        
    # Center the text horizontally
    padding = (width - plain_text_len) // 2
    
    # Prepare display area
    lines = height // 3  # Use 1/3 of terminal height
    display_height = amplitude * 2 + 1
    start_line = (lines - display_height) // 2
    
    # Hide cursor during animation
    _hide_cursor()
    _clear_screen()
    
    colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]
    
    # Calculate total animation steps
    animation_steps = int(plain_text_len * cycles * 2)
    
    # Assume plain text for character access during animation
    plain_text = subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout

    for step in range(animation_steps):
        # Clear the animation area
        for y in range(display_height):
            _move_cursor(1, start_line + y)
            print(" " * width, end="")
            
        for i in range(plain_text_len):
            # Calculate the sine wave position
            phase = step / 10
            wave_height = int(amplitude * math.sin((i/2) + phase))
            y_pos = amplitude + wave_height
            
            # Calculate character position
            screen_x = padding + i
            screen_y = start_line + y_pos
            
            # Skip if outside display area
            if not (0 <= y_pos < display_height):
                continue
                
            # Position cursor and display character
            _move_cursor(screen_x + 1, screen_y + 1)
            
            current_char = plain_text[i] # Access plain text char

            if rainbow:
                # Choose color based on character position
                color_idx = (i + step) % len(colors)
                color = colors[color_idx]
                print(f"{COLORS[color]}{current_char}{COLORS['reset']}", end="", flush=True)
            else:
                print(current_char, end="", flush=True)
                
        time.sleep(speed)
    
    # Clean up
    _clear_screen()
    _show_cursor()
    
    # Display final text centered
    if rainbow:
        color_text = ""
        for i, char in enumerate(plain_text):
            color_idx = i % len(colors)
            color_text += f"{COLORS[colors[color_idx]]}{char}{COLORS['reset']}"
        print(_center_text(color_text))
    else:
        print(_center_text(text)) # Print original text (might have ANSI)

def _progress_bar(text, width=40, progress=0.0, fill_char="•", empty_char="·",
                 bar_color="cyan", text_color="yellow", pulse=False):
    """Show a progress bar with a given progress (0.0 to 1.0)"""
    global VISUAL_MODE
    # Ensure progress is between 0 and 1
    progress = max(0.0, min(1.0, progress))
    
    # Apply pulsing effect if requested (and not in minimal mode)
    if pulse and VISUAL_MODE == "full":
        pulse_factor = abs(math.sin(time.time() * 5))
        filled_width = int(width * progress * (0.8 + 0.2 * pulse_factor))
    else: # Minimal mode or pulse is False
        filled_width = int(width * progress)
    
    # Create bar components
    filled = fill_char * filled_width
    empty = empty_char * (width - filled_width)
    
    # Format colored bar
    bar = f"{COLORS[bar_color]}{filled}{COLORS['reset']}{empty}"
    
    # Format percent
    percent = int(progress * 100)
    
    # Get terminal width
    term_width, _ = _get_terminal_size()
    
    # Format the entire line
    text_display = f" {COLORS[text_color]}{text}{COLORS['reset']}"
    percent_display = f"{COLORS[text_color]}{percent}%{COLORS['reset']}"
    
    # Calculate length considering ANSI escape codes might be present
    plain_text_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout)
    total_width = plain_text_len + len(f" [{bar}] {percent}%") + 1 # +1 for space before text
    
    # Adjust if terminal is too narrow
    if total_width > term_width:
        # Shorten the bar
        excess = total_width - term_width + 3
        width = max(10, width - excess)
        # Recalculate bar with new width
        if pulse and VISUAL_MODE == "full":
             pulse_factor = abs(math.sin(time.time() * 5))
             filled_width = int(width * progress * (0.8 + 0.2 * pulse_factor))
        else:
             filled_width = int(width * progress)
        filled = fill_char * filled_width
        empty = empty_char * (width - filled_width)
        bar = f"{COLORS[bar_color]}{filled}{COLORS['reset']}{empty}"

    print(f"\r{text_display} [{bar}] {percent_display} ", end="", flush=True) # Added trailing space

def _countdown(seconds, text="Starting in", colors=None):
    """Display a cute countdown with optional color cycling."""
    global VISUAL_MODE
    if colors is None:
        colors = ["pink", "purple", "cyan", "blue", "lavender"]

    if VISUAL_MODE == "minimal":
        for i in range(seconds, 0, -1):
            print(f"{text} {i}...")
            time.sleep(1)
        print(f"{text} 0...") # Final message
        time.sleep(0.5)
        return

    _hide_cursor()
    width, _ = _get_terminal_size()
    
    # Create a circular iterator for colors
    color_cycle = 0
    
    for i in range(seconds, 0, -1):
        color = colors[color_cycle % len(colors)]
        color_cycle += 1
        
        # Create countdown text with sparkles and colors
        countdown_text = f"{text} {COLORS[color]}{i}{COLORS['reset']} ✨"
        
        # Center and display
        centered_text = _center_text(countdown_text, width)
        print(f"\r{' ' * width}", end="", flush=True)
        print(f"\r{centered_text}", end="", flush=True)
        
        # Pulse effect
        for _ in range(5):  # 5 pulses per second
            pulse_value = abs(math.sin(time.time() * 10)) * 0.3 + 0.7
            # brightness = int(pulse_value * 255) # Not used
            # We can't actually change brightness easily in terminal,
            # but we can simulate with extra sparkles
            if random.random() < pulse_value * 0.5:
                extra_sparkle = random.choice(["✨", "✧", "✦"])
                print(f"\r{centered_text} {COLORS[color]}{extra_sparkle}{COLORS['reset']}", end="", flush=True)
            else:
                print(f"\r{centered_text}", end="", flush=True)
            time.sleep(0.2)
    
    # Clear the line after countdown
    print(f"\r{' ' * width}", end="", flush=True)
    _show_cursor()

def _spinner(text: str, duration: float = 0.5, spin_type="flower"):
    """Enhanced text-based spinner with fun characters."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        width, _ = _get_terminal_size()
        display = f" {text}..."
        plain_display_len = len(display)
        if plain_display_len > width:
            display = display[:width-3] + "..."
            plain_display_len = len(display)
        print(f"\r{display}", end="", flush=True)
        time.sleep(duration if duration > 0.1 else 0.1) # Still pause briefly
        print(f"\r{' ' * plain_display_len}\r", end="", flush=True) # Clear the line
        return
    spinner_types = {
        "flower": ["✿", "❀", "✾", "❁", "✽", "✼"],
        "star": ["✦", "✧", "✩", "✪", "✫", "✬", "✭", "✮"],
        "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "arrows": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
        "pulse": ["•", "○", "●", "○"],
        "bounce": ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"]
    }
    
    spinner_chars = spinner_types.get(spin_type, spinner_types["flower"])
    colors = ["pink", "purple", "cyan", "blue", "lavender", "mint"]
    
    _hide_cursor()
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        # Oscillate spinner speed using sine wave
        speed_factor = abs(math.sin(i / 10)) * 0.1 + 0.05
        
        # Select spinner character and color
        spinner_char = spinner_chars[i % len(spinner_chars)]
        color_name = colors[i % len(colors)]
        
        # Get terminal width
        width, _ = _get_terminal_size()
        
        # Create display with spinner and text
        display = f" {COLORS[color_name]}{spinner_char}{COLORS['reset']} {text}..."
        
        # Calculate length considering ANSI escape codes might be present
        plain_display_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=display, capture_output=True, text=True).stdout)

        # Make sure it fits
        if plain_display_len > width:
             # Need to truncate carefully if text has ANSI codes
             # Basic truncation for now
             display = display[:width-3] + "..." 
             plain_display_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=display, capture_output=True, text=True).stdout)
            
        # Display
        print(f"\r{' ' * width}", end="\r", flush=True) # Clear with full width
        print(f"\r{display}", end="", flush=True)
        
        time.sleep(speed_factor)
        i += 1
    
    # Clear line using full width
    width, _ = _get_terminal_size()
    print(f"\r{' ' * width}\r", end="", flush=True)
    _show_cursor()

def _print_step(message: str, status: str = "", animate=True):
    """Prints a step message with an optional status indicator."""
    global VISUAL_MODE
    symbols = {
        "success": "✓",
        "warning": "!",
        "error": "✗",
        "info": "✧",
        "progress": "→",
        "star": "★",
        "heart": "♥",
        "note": "•"
    }
    
    colors = {
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "cyan",
        "progress": "blue",
        "star": "purple",
        "heart": "pink",
        "note": "lavender"
    }
    
    # Default symbol and color
    symbol = "   "
    color = "reset"
    
    # Set symbol and color based on status
    if status in symbols:
        symbol = f"[{symbols[status]}]"
        color = colors[status]
        
    # Format the message
    formatted_msg = f"{_color_text(symbol, color)} {message}"
    
    # Calculate terminal width
    width, _ = _get_terminal_size()
    
    # Calculate length considering ANSI escape codes might be present
    plain_msg_len = len(subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=formatted_msg, capture_output=True, text=True).stdout)

    # Make sure message fits in terminal
    if plain_msg_len > width:
        # Truncation needs care with ANSI codes
        # Basic truncation for now
        formatted_msg = formatted_msg[:width-3] + "..."
    
    # Animate text reveal if requested
    if animate and VISUAL_MODE == "full":
        print("\r" + " " * width, end="\r", flush=True)
        _animate_text_reveal(formatted_msg, delay=0.003)
    elif animate and VISUAL_MODE == "minimal": # Minimal mode still uses animate_text_reveal but it's faster
        print("\r" + " " * width, end="\r", flush=True)
        _animate_text_reveal(formatted_msg, delay=0.001, minimal_direct_print=True)
    else: # Not animated or minimal mode with animate=False
        print(formatted_msg)

def _typing_effect(text, speed=0.03, variance=0.02):
    """Simulates typing with realistic timing variations."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        sys.stdout.write(text)
        sys.stdout.flush()
        print()
        time.sleep(0.01) # Minimal pause
        return
    _hide_cursor()
    for char in text:
        # Add some randomness to typing speed for realism
        delay = speed + random.uniform(-variance, variance)
        if delay < 0.001:  # Ensure minimum delay
            delay = 0.001
            
        # Longer pauses for punctuation
        if char in ".!?,:;":
            delay *= 3
            
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    _show_cursor()

def _frame_text(text, style="single", color="pink", padding=1):
    """Create a framed text box."""
    frames = {
        "single": {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
        "double": {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
        "rounded": {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
        "bold": {"tl": "┏", "tr": "┓", "bl": "┗", "br": "┛", "h": "━", "v": "┃"},
        "dotted": {"tl": ".", "tr": ".", "bl": ".", "br": ".", "h": ".", "v": "."},
        "ascii": {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|"},
        "stars": {"tl": "✦", "tr": "✦", "bl": "✦", "br": "✦", "h": "✧", "v": "✧"}
    }
    
    frame_style = frames.get(style, frames["single"])
    
    # Split text into lines
    lines = text.split("\n")
    
    # Find the longest line (considering plain text length)
    max_length = 0
    plain_lines = []
    for line in lines:
         plain_line = subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=line, capture_output=True, text=True).stdout
         max_length = max(max_length, len(plain_line))
         plain_lines.append(plain_line)

    # Create top border
    result = [_color_text(frame_style["tl"] + frame_style["h"] * (max_length + padding * 2) + frame_style["tr"], color)]
    
    # Add padding lines if requested
    if padding > 1:
        for _ in range(padding - 1):
            result.append(_color_text(frame_style["v"] + " " * (max_length + padding * 2) + frame_style["v"], color))
    
    # Add text lines with padding
    for i, line in enumerate(lines):
        padding_spaces = " " * padding
        # Use plain_lines[i] length for calculating extra spaces
        extra_spaces = " " * (max_length - len(plain_lines[i])) 
        result.append(_color_text(frame_style["v"] + padding_spaces + line + extra_spaces + padding_spaces + frame_style["v"], color))
    
    # Add bottom padding if requested
    if padding > 1:
        for _ in range(padding - 1):
            result.append(_color_text(frame_style["v"] + " " * (max_length + padding * 2) + frame_style["v"], color))
    
    # Add bottom border
    result.append(_color_text(frame_style["bl"] + frame_style["h"] * (max_length + padding * 2) + frame_style["br"], color))
    
    return "\n".join(result)

def _get_user_home_dir() -> str:
    """Gets the home directory of the user who invoked sudo, falling back."""
    try:
        # Try getting the home directory of the original user if sudo is used
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            # Attempt to get home dir based on username
            try:
                import pwd
                return pwd.getpwnam(sudo_user).pw_dir
            except (ImportError, KeyError):
                 # Fallback if pwd module not available or user not found
                 pass # Continue to next method
        # Fallback to Path.home() which might be root's home under sudo
        return str(Path.home())
    except Exception:
        # Final fallback
        print("[WARN] Could not reliably determine user home directory, using /tmp for backups.")
        return "/tmp"

def _run_virsh_command(command: List[str], dry_run=False):
    """Runs a virsh command, trying without and then with sudo."""
    if dry_run:
        # In dry run mode, just log the command that would be executed
        _print_step(f"[DRY RUN] Would execute: virsh {' '.join(command)}", "info")
        return
        
    try:
        # Try running directly first (might work if user is in libvirt group)
        result = subprocess.run(["virsh"] + command, check=False, capture_output=True, text=True)
        if result.returncode == 0:
             _print_step(f"Virsh command successful: {' '.join(command)}", "success")
             return
        else:
             # Log the error if it failed without sudo
             _print_step(f"Virsh command failed without sudo (rc={result.returncode}): {' '.join(command)}. Error: {result.stderr.strip()}", "warning")
             # Proceed to try with sudo if necessary, but this script runs detached with sudo anyway
             # The original call from cleanup.py ensures this script runs with sudo.
             # So, direct execution should work if permissions are correct for the root user.
             # If it fails here, it's likely a virsh error, not a permission issue.
             _print_step(f"Virsh command failed: {' '.join(command)}. Error: {result.stderr.strip()}", "error")

    except FileNotFoundError:
         _print_step("Error: 'virsh' command not found. Is libvirt installed and in PATH?", "error")
    except Exception as e:
        _print_step(f"Error running virsh command {' '.join(command)}: {e}", "error")

def _fade_transition(duration=0.5):
    """Create a simple fade transition effect."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        # _clear_screen() # Removed for verbosity
        print() # Add a newline for separation instead of clearing
        time.sleep(0.05) # Brief pause
        return
    _hide_cursor()
    term_width, term_height = _get_terminal_size()
    
    # Characters for gradient effect from light to dark
    chars = " ░▒▓█"
    
    # Fade out
    for char in reversed(chars):
        for y in range(term_height):
            _move_cursor(1, y + 1)
            print(char * term_width, end="", flush=True)
        time.sleep(duration / len(chars))
    
    # Clear screen
    _clear_screen()
    
    # Fade in
    for char in chars:
        for y in range(term_height):
            _move_cursor(1, y + 1)
            print(char * term_width, end="", flush=True)
        time.sleep(duration / len(chars))
    
    _clear_screen()
    _show_cursor()

def _exploding_text(text, duration=1.5):
    """Create an explosion animation with text."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        # _clear_screen() # Removed for verbosity
        # height, _ = _get_terminal_size() # Not needed if not clearing and centering vertically
        # print("\n" * (height // 2 - 1)) # Not needed
        print(_center_text(_color_text(text, "purple")))
        time.sleep(0.1)
        return
    width, height = _get_terminal_size()
    # Calculate length considering ANSI escape codes might be present
    plain_text = subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout
    text_length = len(plain_text)
    center_x = width // 2
    center_y = height // 2
    
    # Characters that will explode outward
    particles = [char for char in plain_text if char.strip()]
    if not particles:  # Ensure we have particles
        particles = ["*", ".", "+", "✦", "✧"]
        
    # Create particle explosion
    explosion = []
    for _ in range(min(50, text_length * 3)):  # Create particles based on text length
        char = random.choice(particles)
        # Random angle and velocity
        angle = random.uniform(0, math.pi * 2)
        velocity = random.uniform(0.5, 2.0)
        # Starting position (slightly randomized around center)
        x = center_x + random.randint(-2, 2)
        y = center_y + random.randint(-1, 1)
        # Random color
        color = random.choice(["pink", "purple", "cyan", "yellow", "green", "blue"])
        explosion.append({
            "char": char,
            "x": x, "y": y,
            "dx": math.cos(angle) * velocity,
            "dy": math.sin(angle) * velocity / 2,  # Slower vertical movement
            "color": color,
            "life": random.uniform(0.5, 1.0)  # Life factor
        })
    
    # Run animation
    _hide_cursor()
    _clear_screen()
    
    # First display the text
    _move_cursor(center_x - text_length // 2 + 1, center_y + 1) # Adjust cursor position
    print(_gradient_text(text)) # Print original text with potential ANSI codes
    time.sleep(0.5)
    
    # Now explode it
    start_time = time.time()
    while time.time() - start_time < duration:
        # Clear screen
        _clear_screen()
        
        # Update and draw particles
        for particle in explosion:
            # Update position
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            
            # Calculate life remaining based on time
            elapsed = (time.time() - start_time) / duration
            if elapsed > particle["life"]:
                continue
                
            # Draw particle
            x, y = int(particle["x"]), int(particle["y"])
            if 0 <= x < width and 0 <= y < height:
                _move_cursor(x + 1, y + 1)
                print(f"{COLORS[particle['color']]}{particle['char']}{COLORS['reset']}", end="", flush=True)
    
    # Clean up and display the text again
    _clear_screen()
    _show_cursor()
    
    # Display final text centered
    print("\n" * (height // 2 - 1))
    print(_center_text(_color_text(text, "purple")))

def _display_floating_particles(duration=2.0):
    """Display floating particle effects in the background."""
    global VISUAL_MODE
    if VISUAL_MODE == "minimal":
        # Do nothing in minimal mode for background effects
        return
    width, height = _get_terminal_size()
    
    # Create particles
    particles = []
    for _ in range(20):  # Create 20 particles
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        char = random.choice(["✨", "✧", "✦", "⋆", "✩", "✫", "*", "·"])
        color = random.choice(["pink", "purple", "cyan", "yellow", "light_blue"])
        dx = random.uniform(-0.3, 0.3)
        dy = random.uniform(-0.15, 0.15)
        particles.append({
            "x": x, "y": y, 
            "char": char, 
            "color": color,
            "dx": dx, "dy": dy
        })
    
    # Run animation
    _hide_cursor()
    _save_cursor_position()
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Update and draw particles
        for p in particles:
            # Erase old position
            _move_cursor(int(p["x"]) + 1, int(p["y"]) + 1)
            print(" ", end="", flush=True)
            
            # Update position with slight randomness
            p["x"] += p["dx"] + random.uniform(-0.1, 0.1)
            p["y"] += p["dy"] + random.uniform(-0.1, 0.1)
            
            # Wrap around screen edges
            p["x"] = p["x"] % width
            p["y"] = p["y"] % height
            
            # Draw new position
            _move_cursor(int(p["x"]) + 1, int(p["y"]) + 1)
            print(f"{COLORS[p['color']]}{p['char']}{COLORS['reset']}", end="", flush=True)
        
        time.sleep(0.1)
    
    # Clean up
    _restore_cursor_position()
    _show_cursor()

def _show_interactive_menu(options, title="Select an option", gradient=True, frame=True):
    """Display an interactive menu and return the selected option with visual enhancements."""
    global VISUAL_MODE
    width, _ = _get_terminal_size()
    
    # Format the title with gradient if requested (simplified for minimal)
    if gradient and VISUAL_MODE == "full":
        title_display = _gradient_text(f"✨ {title} ✨", ["purple", "pink", "cyan"])
    else: # Minimal mode or no gradient
        title_display = _color_text(f"✨ {title} ✨", "purple")
    
    # Build menu content
    menu_content = title_display + "\n\n"
    
    for i, option in enumerate(options):
        option_num = _color_text(str(i+1), "pink", styles=["bold"])
        menu_content += f" {option_num}. {option}\n"
    
    # Frame the menu if requested
    if frame:
        menu_display = _frame_text(menu_content, style="rounded", color="cyan", padding=1)
    else:
        menu_display = menu_content
    
    # Display the menu
    print(menu_display)
    
    # Handle input with visual feedback
    while True:
        choice_prompt = _color_text("\n→ Enter your choice: ", "cyan")
        choice = input(choice_prompt)
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(options):
                # Visual confirmation of selection
                selected_option = options[choice_idx]
                confirmation = f"You selected: {_color_text(selected_option, 'green')}"
                if VISUAL_MODE == "full":
                    _bubble_effect(confirmation, 0.8)
                else: # Minimal mode confirmation
                    print(confirmation)
                    time.sleep(0.2)
                return choice_idx
            print(_color_text("Invalid option. Please try again.", "red"))
        except ValueError:
            print(_color_text("Please enter a number.", "red"))

# --- Dystopian Whirl Effect ---
def _dystopian_whirl_effect(text, duration=4.0): # Increased duration slightly
    """Create a monochromatic, dystopian whirlpool/color wheel effect."""
    global VISUAL_MODE
    # This effect is specifically for full mode. Minimal mode gets a simple print.
    if VISUAL_MODE == "minimal":
        _print_step(text, "success", animate=False)
        return

    _hide_cursor()
    _clear_screen()
    width, height = _get_terminal_size()
    center_x, center_y = width // 2, height // 2

    whirl_chars = ["▓", "▒", "░", "█", "*", "+", ".", "§", "#", "?", "!", "/", "\\"] # Added glitch chars
    noise_chars = [".", ",", "'", "`"]
    # Monochromatic palette (greys)
    dystopia_palette = [
        "\033[38;5;235m",  # Darkest grey
        "\033[38;5;237m",
        "\033[38;5;239m",
        "\033[38;5;241m",  # Medium grey
        "\033[38;5;243m",
        "\033[38;5;245m",
        "\033[38;5;247m",  # Lighter grey
    ]
    text_color_code = "\033[38;5;252m" # Very light grey / off-white for text

    start_time = time.time()
    angle_offset = 0
    num_rings = 5 # Increased number of rings
    ring_spacing = 2 # Reduced spacing slightly
    
    # Ensure max_base_radius is positive
    # Calculate plain text width for radius calculation
    plain_text = subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=text, capture_output=True, text=True).stdout
    max_base_radius = min(center_x, center_y) - (num_rings * ring_spacing) - len(plain_text)//2 - 2
    if max_base_radius < 2: max_base_radius = 2


    text_lines = text.split('\n')
    text_block_height = len(text_lines)
    # Calculate max width of plain text lines
    plain_text_lines = [subprocess.run(['sed', '-r', 's/\x1b\[[0-9;]*m//g'], input=line, capture_output=True, text=True).stdout for line in text_lines]
    text_block_width = max(len(line) for line in plain_text_lines) if plain_text_lines else 0
    text_start_y = center_y - text_block_height // 2

    while time.time() - start_time < duration:
        _clear_screen() # Clear screen each frame for a potentially glitchy/dystopian feel

        # Draw background noise
        for _ in range(width // 10): # Add some sparse noise
             nx = random.randint(0, width - 1)
             ny = random.randint(0, height - 1)
             n_char = random.choice(noise_chars)
             n_color = random.choice(dystopia_palette[:3]) # Use darker greys for noise
             _move_cursor(nx + 1, ny + 1)
             sys.stdout.write(f"{n_color}{n_char}{COLORS['reset']}")

        # Draw whirlpool rings
        for r_idx in range(num_rings):
            # Pulsing and more varying radius for each ring
            base_ring_radius = max_base_radius + r_idx * ring_spacing
            # More distinct pulse/oscillation per ring
            pulse_freq = 1.5 + r_idx * 0.4
            pulse_amp = 1.5 + (r_idx % 2) # Alternate amplitude slightly
            pulse_factor = math.sin(time.time() * pulse_freq + r_idx * math.pi / 3)
            current_radius = base_ring_radius + pulse_factor * pulse_amp
            if current_radius < 1: current_radius = 1
            
            num_points_on_ring = int(current_radius * math.pi * 1.2) # Slightly denser rings
            if num_points_on_ring < 6: num_points_on_ring = 6

            for i in range(num_points_on_ring):
                # Each ring rotates at a more distinct speed/direction
                # Alternate direction for odd/even rings
                direction = 1 if r_idx % 2 == 0 else -1
                speed_factor = 0.8 + (r_idx * 0.15) # Speed increases slightly for outer rings
                current_angle_offset = angle_offset * speed_factor * direction
                angle = (2 * math.pi / num_points_on_ring) * i + current_angle_offset

                x = center_x + int(current_radius * math.cos(angle))
                # Adjust for character aspect ratio (characters are taller than wide) - slightly less squish
                y = center_y + int(current_radius * math.sin(angle) * 0.55)

                if 0 <= y < height and 0 <= x < width:
                    # Basic check to avoid drawing directly over the central text area
                    is_text_area = (text_start_y <= y < text_start_y + text_block_height and
                                    center_x - text_block_width//2 <= x < center_x + text_block_width//2 + text_block_width%2)
                    if is_text_area:
                        continue
                        
                    char_choice = whirl_chars[(i + int(angle_offset * 5) + r_idx*2) % len(whirl_chars)]
                    color_code = dystopia_palette[(i + r_idx + int(time.time() * 10)) % len(dystopia_palette)]

                    _move_cursor(x + 1, y + 1)
                    sys.stdout.write(f"{color_code}{char_choice}{COLORS['reset']}")
        
        # Draw the text in the center, starkly with flicker
        if random.random() > 0.1: # 90% chance to draw text normally
            current_text_color_code = text_color_code
            if random.random() < 0.05: # Small chance for even brighter flicker
                 current_text_color_code = "\033[38;5;255m" # Bright white
        elif random.random() > 0.5: # 5% chance to draw darker
             current_text_color_code = dystopia_palette[-2] # Use a slightly darker grey
        else: # 5% chance to not draw text at all (skip drawing)
             current_text_color_code = None

        if current_text_color_code:
            for line_idx, line_content in enumerate(text_lines):
                line_y = text_start_y + line_idx
                # Use plain text line length for centering
                plain_line_len = len(plain_text_lines[line_idx]) 
                line_x = center_x - plain_line_len // 2
                _move_cursor(line_x + 1, line_y + 1)
                # Add random slight horizontal jitter
                jitter_x = random.randint(-1, 1) if random.random() < 0.03 else 0 
                _move_cursor(line_x + jitter_x + 1, line_y + 1)
                # Print original line content which might have ANSI codes
                sys.stdout.write(f"{COLORS['bold']}{current_text_color_code}{line_content}{COLORS['reset']}")

        sys.stdout.flush()
        angle_offset -= 0.25  # Slightly faster base rotation
        time.sleep(0.05) # Slightly faster frame rate

    _clear_screen()
    _show_cursor()
    
    print("\n" * (height // 3))
    print(_center_text(_color_text(text, text_color_code, styles=["bold"])))
    print("\n" * (height // 3))
    time.sleep(2.0)


# --- Main Execution Logic ---
def main():
    global VISUAL_MODE # Ensure we're using the global
    parser = argparse.ArgumentParser(description="ULTMOS Self-Destruct Script")
    # Define arguments that are ALWAYS needed or optional
    parser.add_argument("--visual-mode", choices=['full', 'minimal'], default="full", help="Visual mode for the script output ('full' or 'minimal')")
    parser.add_argument(
        "--test-animation", 
        choices=[
            'sparkle', 'bubble', 'wave', 'progressbar', 'countdown', 
            'spinner', 'reveal', 'typing', 'fade', 'explode', 
            'particles', 'whirl'
        ],
        default=None,
        help="Run a specific animation test and exit."
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate the cleanup without making actual changes")
    
    # --- Initial parse to check for test mode ---
    # Use parse_known_args to capture known args without failing on missing required ones yet
    args, unknown = parser.parse_known_args() 

    # Determine visual mode early (needed for test mode too)
    if args.visual_mode == "minimal":
        VISUAL_MODE = "minimal"
    # else VISUAL_MODE remains "full" (its default set at the top of the file)

    # --- Animation Test Mode ---
    if args.test_animation:
        _clear_screen()
        _hide_cursor()
        print(f"--- Testing Animation: {args.test_animation} (Mode: {VISUAL_MODE}) ---")
        time.sleep(1)
        
        test_text = f"Testing: {args.test_animation}"
        
        try:
            if args.test_animation == 'sparkle':
                _sparkle_effect(test_text, duration=2.5, density=4)
            elif args.test_animation == 'bubble':
                _bubble_effect(test_text, duration=2.0, speed=0.07)
            elif args.test_animation == 'wave':
                _wave_text(test_text, cycles=2, speed=0.0018, amplitude=2, rainbow=True)
            elif args.test_animation == 'progressbar':
                print("Testing Progress Bar (0% to 100%):")
                for i in range(101):
                    _progress_bar(test_text, progress=i/100.0, pulse=(VISUAL_MODE=='full'))
                    time.sleep(0.03)
                print("\nProgress Bar Test Complete.")
            elif args.test_animation == 'countdown':
                _countdown(5, text=test_text)
            elif args.test_animation == 'spinner':
                print("Testing Spinners:")
                spin_types = ["flower", "star", "dots", "arrows", "pulse", "bounce"]
                for stype in spin_types:
                     _spinner(f"{test_text} ({stype})", duration=1.5, spin_type=stype)
                print("Spinner Test Complete.")
            elif args.test_animation == 'reveal':
                _animate_text_reveal(f"{test_text} (gradient)", gradient=True, center=True)
                _animate_text_reveal(f"{test_text} (rainbow)", rainbow=True, center=True, delay=0.04)
                _animate_text_reveal(f"{test_text} (color)", color="mint", center=True, delay=0.03)
            elif args.test_animation == 'typing':
                _typing_effect(f"{test_text}. This simulates typing with pauses.", speed=0.04, variance=0.03)
            elif args.test_animation == 'fade':
                print("Before fade...")
                _fade_transition(duration=1.0)
                print("...After fade.")
            elif args.test_animation == 'explode':
                _exploding_text(test_text, duration=2.0)
            elif args.test_animation == 'particles':
                print("Displaying floating particles for 3 seconds...")
                _display_floating_particles(duration=3.0)
                print("Floating particles test complete.")
            elif args.test_animation == 'whirl':
                _dystopian_whirl_effect(test_text, duration=4.0)
                
            print(f"\n--- Animation Test '{args.test_animation}' Complete ---")
            
        except Exception as e:
            _show_cursor()
            print(f"\nError during animation test: {e}")
            sys.exit(1)
        finally:
            _show_cursor()
            
        sys.exit(0) # Exit after testing animation

    # --- Normal Execution Logic ---
    # (Only runs if --test-animation was NOT provided)
    # Define arguments required ONLY for normal operation
    parser.add_argument("--directory", required=True, help="Absolute path to the directory to remove")
    parser.add_argument("--keep-disks", required=True, choices=['True', 'False'], help="Whether to keep/backup disks")
    parser.add_argument("--vms", nargs='*', default=[], help="List of VM names to undefine")
    
    # Now, re-parse args fully, enforcing requirements for normal operation
    args = parser.parse_args() 

    target_dir = Path(args.directory).resolve()
    keep_disks_flag = args.keep_disks == 'True'
    vms_to_undefine = args.vms
    backup_dir_base = None

    # --- Display the intro animation ---
    _clear_screen()
    _hide_cursor()
    
    # Show dry run indicator in intro if enabled
    if args.dry_run:
        dry_run_logo = """
 ╭──────────────────────────────────╮
 │  ✨  SIMULATION MODE ACTIVE  ✨  │
 │     No changes will be made      │
 ╰──────────────────────────────────╯
"""
        print(_gradient_text(dry_run_logo, ["yellow", "orange"]))
        time.sleep(1)
    
    # Display main logo with particle effects
    _display_floating_particles(1.0)
    print(_color_text(ULTMOS_LOGO, "pink"))
    
    # Animated title reveal
    _sparkle_effect("ULTMOS CLEANUP UTILITY", 1.5, density=5, colors=["pink", "purple", "cyan", "blue", "lavender"])
    
    # Animated message
    _animate_text_reveal("✨ Starting the gentle cleanup process ✨", delay=0.03, gradient=["pink", "purple", "cyan"], center=True)
    time.sleep(0.5)

    _print_step("Cleanup sequence initiated!", "info")
    if VISUAL_MODE == "full":
        _spinner("Preparing cleanup sequence...", 0.7, spin_type="dots")
    _countdown(3, "Beginning in", colors=["pink", "purple", "cyan", "blue", "lavender"])

    # --- Safety Checks with enhanced visuals ---
    if VISUAL_MODE == "full":
        _fade_transition(0.2) # Short transition
    _print_step("Performing safety checks...", "info")
    
    # Security verification progress with pulsing effect
    for i in range(5):
        progress = (i + 1) / 5
        _progress_bar("Security verification", width=30, progress=progress, 
                     bar_color="cyan", text_color="purple", pulse=True)
        time.sleep(0.3)
    print()
    
    # Enhanced directory validation
    _print_step(f"Validating target directory: {target_dir}", "progress")
    if not target_dir.exists():
        _print_step(f"CRITICAL ERROR: Target directory {target_dir} does not exist.", "error")
        sys.exit(1)
    if not target_dir.is_dir():
        _print_step(f"CRITICAL ERROR: Target path {target_dir} exists but is not a directory.", "error")
        sys.exit(1)
    _print_step("Target directory exists and is a directory.", "success")

    # Check for expected ULTMOS files/folders
    if not (target_dir / "main.py").exists() or not (target_dir / "scripts").is_dir():
         _print_step(f"Error: Target {target_dir} does not look like ULTMOS project (missing main.py or scripts/ folder).", "error")
         # Decide if this is critical enough to exit, or just a warning
         # For now, let's make it critical as per original logic
         sys.exit(1)
    _print_step("ULTMOS project structure check passed.", "success")
    
    _print_step("Safety checks passed.", "success")
    if VISUAL_MODE == "full":
        _bubble_effect("System Verified & Secure", 1.0)
        time.sleep(0.3)

    # --- Interactive Simulation (Dry Run Mode) with enhanced UI ---
    if args.dry_run:
        _print_step("✨ DRY RUN MODE - No actual changes will be made ✨", "star")
        
        # Main simulation menu with improved visuals
        while True:
            # Display a floating header
            _fade_transition(0.3)
            print(_frame_text(SMALL_LOGO, style="rounded", color="pink", padding=1))
            print()
            
            options = [
                "Simulate removing project directory",
                "Simulate backing up disk images",
                "Simulate undefining VMs",
                "View target details",
                "Exit simulation"
            ]
            choice = _show_interactive_menu(options, "SIMULATION MENU")
            
            if choice == 0:  # Simulate removing directory
                _print_step(f"[SIMULATION] Would remove directory: {target_dir}", "info")
                _countdown(3, "Simulating deletion in", colors=["yellow", "orange", "red"])
                
                total_steps = 10
                for i in range(total_steps):
                    _progress_bar("Simulating file removal", width=40, progress=(i+1)/total_steps, 
                                 bar_color="red", text_color="yellow", pulse=True)
                    delay = abs(math.sin(i/2)) * 0.3 + 0.1
                    time.sleep(delay)
                print()
                
                _print_step(f"[SIMULATION] Directory {target_dir} would be removed.", "success")
                _bubble_effect("No files were actually deleted", 1.5)
                
            elif choice == 1:  # Simulate backup
                if keep_disks_flag:
                    _print_step("[SIMULATION] Would backup disk images", "info")
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    home_dir = _get_user_home_dir()
                    backup_location = Path(home_dir) / f"ultmos_backups_{timestamp}"
                    
                    # Show the backup location with visual emphasis
                    location_msg = f"[SIMULATION] Would create backup in:"
                    path_display = f"{backup_location}"
                    _print_step(location_msg, "info", animate=False)
                    _typing_effect(f"  {_color_text(path_display, 'green')}", speed=0.01)
                    
                    _wave_text("Simulating disk backup...", cycles=2, amplitude=2, rainbow=True)
                    
                    # Show a more visually interesting progress animation
                    print()
                    for i in range(20):
                        progress = math.sin(i / 20 * math.pi) * 0.2 + (i / 20 * 0.8)  # Non-linear progress
                        _progress_bar("Simulating backup process", width=35, progress=progress, 
                                     bar_color="cyan", text_color="blue")
                        time.sleep(0.1)
                    print()
                    
                    _print_step("[SIMULATION] Files that would be backed up:", "info")
                    backup_files = [
                        str(target_dir / "disks"),
                        str(target_dir / "BaseSystem.img"),
                        str(target_dir / "BaseSystem.dmg"),
                        str(target_dir / "HDD.qcow2")
                    ]
                    
                    # Animate the file list
                    for file in backup_files:
                        if Path(file).exists():
                            _spinner(f"Checking {Path(file).name}", 0.3, spin_type="star")
                            _print_step(f" - {file}", "success")
                        else:
                            _spinner(f"Checking {Path(file).name}", 0.3, spin_type="dots")
                            _print_step(f" - {file} (not found)", "warning")
                    
                    _exploding_text("Backup Simulation Complete!", 1.0)
                else:
                    _print_step("[SIMULATION] Keep-disks flag is False, would not backup.", "warning")
                
            elif choice == 2:  # Simulate VM undefine
                if vms_to_undefine:
                    _print_step("[SIMULATION] Would undefine the following VMs:", "info")
                    
                    # Create more engaging VM simulation
                    for i, vm in enumerate(vms_to_undefine):
                        # Progress through different spinner types for variety
                        spinner_types = ["flower", "star", "dots", "pulse", "arrows", "bounce"]
                        spinner_type = spinner_types[i % len(spinner_types)]
                        
                        _spinner(f"Simulating undefine of VM: {vm}", 0.8, spin_type=spinner_type)
                        
                        # Use a color gradient for the VM name
                        vm_display = _gradient_text(vm, ["cyan", "blue", "purple"])
                        status_display = _color_text('[Simulated]', 'pink')
                        _print_step(f" - {vm_display} {status_display}", "success")
                    
                    # Show VM undefine flags with visual separation
                    print()
                    _print_step("[SIMULATION] VMs would be undefined with these flags:", "info")
                    
                    # Use a fancy framed display for flags
                    undefine_flags = ["--nvram"]
                    if not keep_disks_flag:
                        undefine_flags.append("--remove-all-storage")
                        flags_info = "  --nvram\n  --remove-all-storage (Will delete storage!)"
                        _print_step("  - With storage removal", "warning")
                    else:
                        flags_info = "  --nvram (Preserving storage)"
                        _print_step("  - Without storage removal", "success")
                    
                    print(_frame_text(flags_info, style="dotted", color="yellow", padding=1))
                else:
                    _print_step("[SIMULATION] No VMs to undefine specified.", "info")
                
            elif choice == 3:  # View target details with improved visualization
                _clear_screen()
                _print_step("Target directory information:", "info")
                
                # Create a more visually appealing directory info display
                if target_dir.exists():
                    # Animate the path reveal
                    _print_step("Path:", "note", animate=False)
                    _typing_effect(f"  {_color_text(str(target_dir), 'green')}", speed=0.01)
                    
                    try:
                        # Count files with animation
                        _spinner("Analyzing directory structure", 1.0, spin_type="dots")
                        
                        # Count files and subdirectories
                        file_count = sum(1 for _ in target_dir.rglob('*') if _.is_file())
                        dir_count = sum(1 for _ in target_dir.rglob('*') if _.is_dir())
                        
                        # Create a fancy display
                        stats_display = f"""
 Files:       {_color_text(str(file_count), 'cyan')}
 Directories: {_color_text(str(dir_count), 'purple')}
 """
                        print(_frame_text(stats_display, style="single", color="blue", padding=1))
                        
                        # Calculate size with a progress animation
                        print()
                        _print_step("Calculating size...", "progress")
                        
                        total_size = 0
                        scanned_files = 0
                        max_files = 1000  # Limit for performance
                        
                        for i, _ in enumerate(target_dir.rglob('*')):
                            if i > max_files:  # Limit the files we check for speed
                                break
                            if _.is_file():
                                total_size += _.stat().st_size
                                scanned_files += 1
                                if scanned_files % 50 == 0:  # Update progress every 50 files
                                    progress = min(1.0, scanned_files / max_files)
                                    _progress_bar("Scanning files", width=30, progress=progress, 
                                                 bar_color="blue", text_color="cyan")
                        print()
                        
                        # Display size in appropriate units
                        if total_size < 1024:
                            size_str = f"{total_size} bytes"
                        elif total_size < 1024 * 1024:
                            size_str = f"{total_size / 1024:.2f} KB"
                        elif total_size < 1024 * 1024 * 1024:
                            size_str = f"{total_size / (1024 * 1024):.2f} MB"
                        else:
                            size_str = f"{total_size / (1024 * 1024 * 1024):.2f} GB"
                        
                        size_msg_fancy = f"\n Estimated size: {_color_text(size_str, 'green')} (sampled)\n"
                        print(_frame_text(size_msg_fancy, style="stars", color="cyan", padding=1))
                        
                    except Exception as e:
                        _print_step(f"Error analyzing directory: {e}", "error")
                else:
                    _print_step(f"Target directory {target_dir} does not exist.", "error")
                
                # Wait for user to press Enter to continue
                input(_color_text("\n Press Enter to return to menu...", "lavender"))
                
            elif choice == 4:  # Exit simulation with fancy animation
                _sparkle_effect("Exiting Simulation", 1.0)
                _animate_text_reveal("Thank you for using ULTMOS Cleanup Utility", delay=0.04, 
                                   gradient=["green", "cyan", "blue"], center=True)
                _print_step("Dry run complete. No changes were made.", "success")
                sys.exit(0)

        # End simulation - we never actually reach this due to the sys.exit() in the menu
        sys.exit(0)

    # Safety check - this ensures that even if the above exit is somehow bypassed, 
    # no actual operations will run in dry run mode
    if args.dry_run:
        _print_step("Dry run complete - no changes were made.", "success")
        sys.exit(0)

    # --- Undefine VMs with enhanced UI ---
    if vms_to_undefine:
        if VISUAL_MODE == "full" and not args.dry_run: # Add transition only if not in dry_run
            _fade_transition(0.4)
        _print_step("Attempting to undefine VMs from libvirt...", "info")
        undefine_flags = ["--nvram"]
        if not keep_disks_flag:
            undefine_flags.append("--remove-all-storage")
            _print_step("(Including associated storage)")

        # Visual divider
        print(_color_text("┄" * 40, "purple"))
        
        for i, vm_name in enumerate(vms_to_undefine):
            _spinner(f"Processing VM: {vm_name}", 0.8, spin_type="arrows")
            _progress_bar(f"VM {i+1}/{len(vms_to_undefine)}", width=20, 
                         progress=(i+1)/len(vms_to_undefine),
                         bar_color="purple", text_color="cyan")
            print()
            _run_virsh_command(["destroy", vm_name], dry_run=args.dry_run)
            _run_virsh_command(["undefine", vm_name] + undefine_flags, dry_run=args.dry_run)
        
        # Visual completion effect
        _print_step("VM undefine attempts complete.", "success")
        _bubble_effect("All VMs processed", 1.0)

    # --- Backup/Handle Disks with enhanced feedback ---
    if keep_disks_flag:
        # Clear screen for this major step
        _fade_transition(0.3)
        
        title = "DISK BACKUP"
        print(_frame_text(title, style="double", color="cyan", padding=1))
        
        _print_step("Attempting to backup disk images...", "info")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        home_dir = _get_user_home_dir()
        backup_dir_base = Path(home_dir) / f"ultmos_backups_{timestamp}"
        disks_dir_path = target_dir / "disks"
        basesystem_img_path = target_dir / "BaseSystem.img"
        basesystem_dmg_path = target_dir / "BaseSystem.dmg"
        hdd_qcow2_path = target_dir / "HDD.qcow2"

        try:
            if not args.dry_run:
                backup_dir_base.mkdir(parents=True, exist_ok=True)
            
            # Show backup location with visual effect
            location_msg = f"Backup location:"
            _print_step(location_msg, "note", animate=False)
            _typing_effect(f"  {_color_text(str(backup_dir_base), 'green')}", speed=0.015)
    
            if disks_dir_path.is_dir():
                _wave_text("Backing up disk directory...", cycles=2, amplitude=2, rainbow=True)
                try:
                    if not args.dry_run:
                        shutil.copytree(disks_dir_path, backup_dir_base / disks_dir_path.name, dirs_exist_ok=True)
                        _print_step(f"✓ Directory '{disks_dir_path.name}' backed up successfully", "success")
                    else:
                        _print_step(f"Would backup directory: {disks_dir_path}", "info")
                except (shutil.Error, PermissionError) as e:
                    _print_step(f"Failed to backup directory {disks_dir_path}: {e}", "error")
    
            # Visual separator
            print(_color_text("┄" * 40, "purple"))
            
            # Handle BaseSystem files with better feedback
            copied_basesystem = False
            if basesystem_img_path.is_file():
                _spinner(f"Backing up {basesystem_img_path.name}...", 0.8, spin_type="pulse")
                try:
                    if not args.dry_run:
                        shutil.copy2(basesystem_img_path, backup_dir_base / basesystem_img_path.name)
                        _print_step(f"✓ {basesystem_img_path.name} backed up", "success")
                    else:
                        _print_step(f"Would backup: {basesystem_img_path.name}", "info")
                    copied_basesystem = True
                except (FileNotFoundError, PermissionError) as e:
                    _print_step(f"Failed to backup {basesystem_img_path.name}: {e}", "error")
                    
            if not copied_basesystem and basesystem_dmg_path.is_file():
                _spinner(f"Backing up {basesystem_dmg_path.name}...", 0.8, spin_type="pulse")
                try:
                    if not args.dry_run:
                        shutil.copy2(basesystem_dmg_path, backup_dir_base / basesystem_dmg_path.name)
                        _print_step(f"✓ {basesystem_dmg_path.name} backed up", "success")
                    else:
                        _print_step(f"Would backup: {basesystem_dmg_path.name}", "info")
                except (FileNotFoundError, PermissionError) as e:
                    _print_step(f"Failed to backup {basesystem_dmg_path.name}: {e}", "error")

            # Handle HDD file
            if hdd_qcow2_path.is_file():
                _spinner(f"Backing up {hdd_qcow2_path.name}...", 0.8, spin_type="dots")
                try:
                    if not args.dry_run:
                        shutil.copy2(hdd_qcow2_path, backup_dir_base / hdd_qcow2_path.name)
                        _print_step(f"✓ {hdd_qcow2_path.name} backed up", "success")
                    else:
                        _print_step(f"Would backup: {hdd_qcow2_path.name}", "info")
                except (FileNotFoundError, PermissionError) as e:
                    _print_step(f"Failed to backup {hdd_qcow2_path.name}: {e}", "error")

            # Visual completion indication
            _exploding_text("Disk Backup Complete!", 1.0)
            
        except Exception as e:
            _print_step(f"Error during disk backup: {e}", "error")

    # --- Remove Project Directory with dramatic countdown ---
    _fade_transition(0.3)
    print(_frame_text("⚠️ DIRECTORY REMOVAL ⚠️", style="double", color="red", padding=1))
    
    dir_message = f"Removing project directory: {target_dir}..."
    _print_step(dir_message, "warning")
    
    # More dramatic countdown for deletion
    print()
    if VISUAL_MODE == "full":
        _countdown(6, "Beginning deletion in", colors=["red", "orange", "yellow"])
    else:
        _countdown(5, "Beginning deletion in", colors=["red", "orange", "yellow"])
    
    # Progress bar with pulsing effect during removal
    total_steps = 15
    for i in range(total_steps):
        _progress_bar("Erasing files", width=40, progress=(i+1)/total_steps, 
                    bar_color="red", text_color="yellow", pulse=True)
        # Variable delay to make it look like it's working on different size files
        delay = 0.1 + abs(math.sin(i/2)) * 0.4 
        time.sleep(delay)
    print()
    
    try:
        if not args.dry_run:
            shutil.rmtree(target_dir, ignore_errors=True)
        _print_step("Directory removal command executed.", "success")
    except Exception as e:
        _print_step(f"Error removing directory: {e}", "error")

    # --- Verify Removal with better visual feedback ---
    _print_step("Verifying removal...")
    _spinner("Scanning filesystem", 1.5, spin_type="bounce")
    time.sleep(1)
    
    if target_dir.exists():
        _print_step("Warning: Project directory may still exist.", "warning")
        subfolder_message = "Some files or folders may require manual removal"
        _animate_text_reveal(subfolder_message, delay=0.03, color="yellow", center=True)
    else:
        _print_step("Project directory removed successfully.", "success")
        success_message = "All files have been deleted"
        _bubble_effect(success_message, 1.0)

    # --- Final Messages with better visual presentation ---
    if keep_disks_flag and backup_dir_base:
        # Show backup summary in a frame
        backup_summary = f"\n Disk images were backed up to:\n {_color_text(str(backup_dir_base), 'green')}\n"
        print(_frame_text(backup_summary, style="rounded", color="cyan", padding=1))
    
    # Final animation
    print()
    _sparkle_effect("ULTMOS UNINSTALLATION COMPLETE", 2.0, density=5,
                   colors=["green", "cyan", "blue", "purple"])
    
    if VISUAL_MODE == "full":
        time.sleep(0.7) # Pause for completion message to sink in

    # Extra thank you message
    thank_you = "Thank you for using ULTMOS"
    _animate_text_reveal(thank_you, delay=0.05, gradient=["green", "cyan", "blue"], center=True)

    # --- Self Destruct with fancy animation ---
    try:
        if VISUAL_MODE == "full":
            _wave_text("Removing self-destruct script...", cycles=20, speed=0.0015, amplitude=2, rainbow=True)
        else: # Minimal mode wave
            _wave_text("Removing self-destruct script...", cycles=15, rainbow=True) # Original minimal parameters
        current_script_path = Path(sys.argv[0]).resolve()
        if not args.dry_run:
            current_script_path.unlink(missing_ok=True)
            if VISUAL_MODE == "full":
                _dystopian_whirl_effect("Self-destruct script removed.", duration=3.5)
            else: # Minimal mode
                _print_step("Self-destruct script removed.", "success", animate=False)
        else:
            _print_step("Would remove self-destruct script.", "info")
    except Exception as e:
        print(f"Warning: Could not remove self-destruct script {current_script_path}: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        _show_cursor()  # Ensure cursor is visible if script is interrupted
        _clear_screen()
        print(_frame_text("\n Operation cancelled by user \n", style="rounded", color="yellow", padding=1))
        sys.exit(1)
    except Exception as e:
        _show_cursor()  # Ensure cursor is visible on error
        print(_color_text(f"\n✗ Error: {e}", "red"))
        sys.exit(1)
    finally:
        _show_cursor()  # Make absolutely sure the cursor is visible when we exit
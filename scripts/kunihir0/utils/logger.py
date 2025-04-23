#!/usr/bin/env python3

"""
Centralized logging system for the kunihir0 utilities.

This module provides standardized logging and output formatting
for the kunihir0 utilities, ensuring consistent error reporting
and user feedback across all components.

Features:
- Type-safe logging functions with proper type hints
- Color-coded output based on message type
- Configurable verbosity levels
- Support for different output formats
"""

from pathlib import Path
from typing import Optional, Union, Any, TextIO, Literal
import sys
from enum import Enum
import traceback


class LogLevel(Enum):
    """Log levels for controlling verbosity."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    SUCCESS = 5


class LogColor:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Logger:
    """Centralized logger for kunihir0 utilities."""
    
    def __init__(
        self,
        min_level: LogLevel = LogLevel.INFO,
        use_colors: bool = True,
        output_stream: TextIO = sys.stdout,
        prefix: str = "kunihir0"
    ):
        """Initialize the logger.
        
        Args:
            min_level: Minimum log level to display
            use_colors: Whether to use colorized output
            output_stream: Where to write log messages
            prefix: Prefix for all log messages
        """
        self.min_level = min_level
        self.use_colors = use_colors
        self.output_stream = output_stream
        self.prefix = prefix
        
    def _should_log(self, level: LogLevel) -> bool:
        """Check if a message at the given level should be logged.
        
        Args:
            level: The log level to check
            
        Returns:
            True if the message should be logged
        """
        return level.value >= self.min_level.value
        
    def _format_message(self, message: str, level: LogLevel) -> str:
        """Format a message with appropriate colors and prefix.
        
        Args:
            message: The message to format
            level: The log level
            
        Returns:
            Formatted message string
        """
        if not self.use_colors:
            return f"[{self.prefix}] [{level.name}] {message}"
            
        color = LogColor.RESET
        
        if level == LogLevel.DEBUG:
            color = LogColor.GRAY
        elif level == LogLevel.INFO:
            color = LogColor.BLUE
        elif level == LogLevel.WARNING:
            color = LogColor.YELLOW
        elif level == LogLevel.ERROR:
            color = LogColor.RED
        elif level == LogLevel.CRITICAL:
            color = LogColor.RED + LogColor.BOLD
        elif level == LogLevel.SUCCESS:
            color = LogColor.GREEN
            
        prefix_color = LogColor.CYAN
        level_str = f"[{level.name}]"
        
        return f"{prefix_color}[{self.prefix}]{LogColor.RESET} {color}{level_str} {message}{LogColor.RESET}"
        
    def log(self, message: str, level: LogLevel) -> None:
        """Log a message at the specified level.
        
        Args:
            message: The message to log
            level: The log level
        """
        if not self._should_log(level):
            return
            
        formatted = self._format_message(message, level)
        print(formatted, file=self.output_stream)
        
    def debug(self, message: str) -> None:
        """Log a debug message.
        
        Args:
            message: The message to log
        """
        self.log(message, LogLevel.DEBUG)
        
    def info(self, message: str) -> None:
        """Log an info message.
        
        Args:
            message: The message to log
        """
        self.log(message, LogLevel.INFO)
        
    def warning(self, message: str) -> None:
        """Log a warning message.
        
        Args:
            message: The message to log
        """
        self.log(message, LogLevel.WARNING)
        
    def error(self, message: str, exception: Optional[Exception] = None) -> None:
        """Log an error message with optional exception information.
        
        Args:
            message: The error message to log
            exception: Optional exception that caused the error
        """
        if exception:
            error_type = type(exception).__name__
            error_msg = str(exception)
            full_message = f"{message}: {error_type} - {error_msg}"
        else:
            full_message = message
            
        self.log(full_message, LogLevel.ERROR)
        
    def critical(self, message: str, exception: Optional[Exception] = None) -> None:
        """Log a critical error message.
        
        Args:
            message: The critical error message to log
            exception: Optional exception that caused the error
        """
        if exception:
            error_type = type(exception).__name__
            error_msg = str(exception)
            full_message = f"{message}: {error_type} - {error_msg}"
            
            if self._should_log(LogLevel.DEBUG):
                # In debug mode, also print traceback
                tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
                full_message += "\n" + "".join(tb)
        else:
            full_message = message
            
        self.log(full_message, LogLevel.CRITICAL)
        
    def success(self, message: str) -> None:
        """Log a success message.
        
        Args:
            message: The success message to log
        """
        self.log(message, LogLevel.SUCCESS)

    def exception(self, message: str, exception: Exception) -> None:
        """Log an exception with traceback.
        
        Args:
            message: Contextual message explaining what operation failed
            exception: The exception that was caught
        """
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        # Format the basic error message
        basic_msg = f"{message}: {error_type} - {error_msg}"
        
        # In debug mode, add traceback information
        if self._should_log(LogLevel.DEBUG):
            tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
            full_message = basic_msg + "\n" + "".join(tb)
            self.log(full_message, LogLevel.ERROR)
        else:
            self.log(basic_msg, LogLevel.ERROR)

    def file_operation(
        self, 
        operation: Literal["create", "read", "write", "delete", "move", "copy"], 
        path: Union[str, Path], 
        success: bool, 
        error: Optional[Exception] = None
    ) -> None:
        """Log a file operation result.
        
        Args:
            operation: Type of file operation
            path: Path that was operated on
            success: Whether the operation succeeded
            error: Optional exception if operation failed
        """
        path_str = str(path)
        
        if success:
            self.success(f"File {operation} successful: {path_str}")
        else:
            if error:
                self.error(f"File {operation} failed: {path_str}", error)
            else:
                self.error(f"File {operation} failed: {path_str}")
                
    def command_result(
        self, 
        command: str, 
        success: bool, 
        stdout: str = "", 
        stderr: str = ""
    ) -> None:
        """Log a command execution result.
        
        Args:
            command: Command that was executed (for display)
            success: Whether the command succeeded
            stdout: Command standard output
            stderr: Command standard error
        """
        if success:
            if stdout.strip():
                self.success(f"Command '{command}' executed successfully")
                if self._should_log(LogLevel.DEBUG):
                    self.debug(f"Output: {stdout.strip()}")
            else:
                self.success(f"Command '{command}' executed successfully")
        else:
            self.error(f"Command '{command}' failed: {stderr.strip()}")


# Create a default logger instance for easy import
default_logger = Logger()

# Convenience functions that use the default logger
def debug(message: str) -> None:
    """Log a debug message using the default logger."""
    default_logger.debug(message)

def info(message: str) -> None:
    """Log an info message using the default logger."""
    default_logger.info(message)

def warning(message: str) -> None:
    """Log a warning message using the default logger."""
    default_logger.warning(message)

def error(message: str, exception: Optional[Exception] = None) -> None:
    """Log an error message using the default logger."""
    default_logger.error(message, exception)

def critical(message: str, exception: Optional[Exception] = None) -> None:
    """Log a critical error message using the default logger."""
    default_logger.critical(message, exception)

def success(message: str) -> None:
    """Log a success message using the default logger."""
    default_logger.success(message)

def exception(message: str, exception: Exception) -> None:
    """Log an exception with traceback using the default logger."""
    default_logger.exception(message, exception)

def file_operation(
    operation: Literal["create", "read", "write", "delete", "move", "copy"], 
    path: Union[str, Path], 
    success: bool, 
    error: Optional[Exception] = None
) -> None:
    """Log a file operation result using the default logger."""
    default_logger.file_operation(operation, path, success, error)

def command_result(
    command: str, 
    success: bool, 
    stdout: str = "", 
    stderr: str = ""
) -> None:
    """Log a command execution result using the default logger."""
    default_logger.command_result(command, success, stdout, stderr)

def set_log_level(level: LogLevel) -> None:
    """Set the minimum log level for the default logger."""
    default_logger.min_level = level

def use_colors(enabled: bool) -> None:
    """Enable or disable colored output for the default logger."""
    default_logger.use_colors = enabled
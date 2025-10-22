"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Centralized logging configuration for Nova framework
"""

import logging
import os
from typing import Optional

# Default log level from environment or INFO
DEFAULT_LOG_LEVEL = os.environ.get("NOVA_LOG_LEVEL", "INFO").upper()

# Valid log levels
VALID_LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logger(name: str = "nova") -> logging.Logger:
    """
    Get a configured logger instance for Nova framework.

    Args:
        name: Logger name (defaults to 'nova')

    Returns:
        Configured logger instance

    Environment Variables:
        NOVA_LOG_LEVEL: Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        NOVA_LOG_FORMAT: Custom log format string
    """
    logger = logging.getLogger(name)

    # Only configure if no handlers exist (avoid duplicate handlers)
    if not logger.handlers:
        # Get log level from environment or use default
        log_level_str = os.environ.get("NOVA_LOG_LEVEL", DEFAULT_LOG_LEVEL)
        log_level = VALID_LOG_LEVELS.get(log_level_str, logging.INFO)
        logger.setLevel(log_level)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Get format from environment or use default
        log_format = os.environ.get(
            "NOVA_LOG_FORMAT",
            "[%(levelname)s] %(message)s"
        )

        # Create formatter
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

        # Prevent propagation to root logger
        logger.propagate = False

    return logger


def set_log_level(level: str) -> None:
    """
    Set the log level for all Nova loggers.

    Args:
        level: Log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Raises:
        ValueError: If level is not a valid log level
    """
    level_upper = level.upper()
    if level_upper not in VALID_LOG_LEVELS:
        raise ValueError(
            f"Invalid log level: {level}. "
            f"Valid levels: {', '.join(VALID_LOG_LEVELS.keys())}"
        )

    log_level = VALID_LOG_LEVELS[level_upper]

    # Update all Nova loggers
    for logger_name in logging.Logger.manager.loggerDict:
        if logger_name.startswith("nova"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(log_level)
            for handler in logger.handlers:
                handler.setLevel(log_level)


# Create default logger instance
logger = get_logger("nova")

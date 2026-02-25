"""Centralized logging setup."""

from __future__ import annotations

import logging
import sys


def setup_logger(name: str, *, level: str = "INFO") -> logging.Logger:
    """Build a configured logger for an agent or module.

    Args:
        name: Logger namespace.
        level: Logging level as string.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

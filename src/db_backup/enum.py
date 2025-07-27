# ==============================================================================
#  Copyright (c) 2025, Nimbus Operations Inc.
# ==============================================================================
from enum import Enum


class LogLevel(str, Enum):
    """Log level."""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

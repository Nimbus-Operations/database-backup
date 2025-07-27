# ==============================================================================
#  Copyright (c) 2025, Nimbus Operations Inc.
# ==============================================================================
"""Logging functions."""

import argparse
import logging
import logging.config
import sys

from typing import Optional

from db_backup.config import _DEFAULTS, Settings
from db_backup.enum import LogLevel


def configure_logging(settings: Optional[Settings], args: Optional[argparse.Namespace]) -> None:
    """Configure logging."""
    log_level = settings.general.debug_level
    log_time = _DEFAULTS['log_time']

    if args.cron:
        log_level = LogLevel.WARNING
        log_time = "%Y-%m-%d %H:%M:%S.%f"

    if args.debug:
        log_level = LogLevel.DEBUG

    # noinspection SpellCheckingInspection
    _logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': _DEFAULTS['log_format'],
                'datefmt': log_time,
            },
        },
        'handlers': {
            'console': {
                'level': str(log_level),
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': sys.stdout,
            }
        },
        'root': {
            'handlers': ['console'],
        }
    }

    logging.config.dictConfig(_logging_config)

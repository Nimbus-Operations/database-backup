# ==============================================================================
#  Copyright (c) 2025, Nimbus Operations Inc.
# ==============================================================================
"""Program entry point."""

import argparse
import inspect
import pathlib
import sys

from typing import Optional

from db_backup import __version__
from .config import _DEFAULTS, Settings
from .log import configure_logging


def parse_args(cli_args: Optional[list] = None) -> argparse.Namespace:
    """Parse command line arguments.

    If cli_args is None, command line arguments are collected from sys.argv.

    Arguments:
        cli_args (list): List of CLI arguments or None.
    """
    args = cli_args or sys.argv[1:]
    parser = argparse.ArgumentParser(
        description=inspect.cleandoc(
            """
            Manages routine backups of individual databases.
            """
        )
    )

    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file.',
        type=pathlib.Path,
        metavar='PATH',
        default=_DEFAULTS['config_path'],
    )
    parser.add_argument(
        '--cron',
        help="Sets output options for execution from cron.",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-d', '--debug',
        help='Enable debug output.',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
    )

    return parser.parse_args(args)


def main():
    """Program entry point."""
    args = parse_args()
    settings = Settings.from_toml(args.config)
    configure_logging(settings, args)


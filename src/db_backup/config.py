# ==============================================================================
#  Copyright (c) 2025, Nimbus Operations Inc.
# ==============================================================================
"""Application configuration."""
import logging
import pathlib
import sys
import tomllib
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings

_LOG = logging.getLogger(__name__)

# noinspection SpellCheckingInspection
_DEFAULTS = {
    'default_keep': 7,
    'log_level': "INFO",
    'log_format': '%(asctime)s %(message)s',
    'log_time': '%H:%M:%S',
    'config_path': '/etc/database-backup.toml'
}


_SETTINGS: Optional['Settings'] = None


class GeneralSettings(BaseModel):
    """General settings for database backup.

    The default_* values which are defined (and not None) will be used as the default for all
    backed-up databases.  These settings can be overridden on a per-database basis.

    Args:
        backup_directory (str): The directory to store backups in.
        default_driver (str): The default driver to use.  Must have a corresponding driver defined.
        default_server (str): The default server to connect to.
        default_user (str): The default user to connect as.
        default_password (str): The default password to use.
        default_keep (int): The default number of backups to keep.
        default_schedule (str): The default schedule to run backups on.
    """
    backup_directory: pathlib.Path = pathlib.Path('/var/local/backups')
    default_driver: Optional[str] = 'postgres'
    default_server: Optional[str] = 'localhost'
    default_user: Optional[str] = None
    default_password: Optional[str] = None
    default_keep: Optional[int] = None
    default_schedule: Optional[str] = None


class DriverSettings(BaseModel):
    """Settings for a database driver.

    Args:
        dump_binary (str): The path to the dump binary.
    """
    dump_binary: pathlib.Path


class DatabaseSettings(BaseModel):
    """Settings for an individual database to back up.

    Args:
        active (bool): Whether the database should be backed up.
        server (str): The server to connect to.
        driver: (str): The driver to use.  Must have a corresponding driver defined.
        user (str): The user to connect as.
        password (str): The password to use.
        keep (int): The number of backups to keep.
        schedule (str): The schedule to run backups on.
    """
    active: bool = True
    server: Optional[str] = None
    driver: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    keep: int = _DEFAULTS['default_keep']
    schedule: Optional[str] = None


class Settings(BaseSettings):
    """Settings for the application."""
    general: GeneralSettings = GeneralSettings()
    driver: dict[str, DriverSettings] = {}
    database: dict[str, DatabaseSettings] = {}

    @classmethod
    def from_toml(cls, path: pathlib.Path) -> 'Settings':
        """Load settings from a TOML file."""
        try:
            with open(path, 'rb') as settings_file:
                settings_data = tomllib.load(settings_file)
        except FileNotFoundError as err:
            _LOG.error(f'Could not load settings from {path}: {err.strerror}')
            sys.exit(1)

        # Construct a mapping of every 'value' -> 'default_value' relationship to set up defaults.
        default_mapping = {}
        for key in settings_data['general']:
            if key.startswith('default_'):
                new_key = key.replace('default_', '')
                default_mapping[new_key] = settings_data['general'][key]

        for _, database in settings_data['database'].items():
            for key in default_mapping:
                if key not in database and default_mapping[key] is not None:
                    database[key] = default_mapping[key]

        return cls.model_validate(settings_data)
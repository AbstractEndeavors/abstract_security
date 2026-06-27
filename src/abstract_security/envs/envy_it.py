from .imports import *
from .abstractEnv import abstractEnv
from .utils import *


def get_env_value(key=None, path=None, file_name=None, deep_scan=False):
    """
    Retrieve the value of `key` from a .env file.

    Args:
        key: The key to search for in the .env file.
        path: A directory or direct path to the .env file.
        file_name: The name of the .env file.
        deep_scan: Allow fuzzy (partial) matching of the key.

    Returns:
        The value of the environment variable if found, otherwise None.
    """
    return abstractEnv(key=key, file_name=file_name, path=path, deep_scan=deep_scan).env_value


def get_env_path(key=None, path=None, file_name=None, deep_scan=False):
    """
    Resolve the path of the .env file that contains `key`.

    Returns:
        The path to the matching .env file if found, otherwise None.
    """
    return abstractEnv(key=key, file_name=file_name, path=path, deep_scan=deep_scan).env_path

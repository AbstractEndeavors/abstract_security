from .imports import *


def split_eq(line):
    """
    Split a line at the first '=' into a [key, value] pair, trimming
    surrounding whitespace.

    Returns [line, None] if no '=' is present.
    """
    if '=' in line:
        key, _, value = line.partition('=')
        return [key.strip(), value.strip()]
    return [line, None]


def search_for_env_key(key, path):
    """
    Return the value of `key` in the .env file at `path`, or None if the file
    does not exist or the key is not present.
    """
    if not path or not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        for line in f:
            line_key, line_value = split_eq(line)
            if line_key == key:
                return line_value
    return None


def check_env_file(path, file_name=DEFAULT_FILE_NAME):
    """
    Return the full path to the env file if it exists, otherwise False.
    """
    if not path:
        return False
    if not str(path).endswith(file_name):
        path = os.path.join(str(path), file_name)
    return path if os.path.isfile(path) else False


def find_and_read_env_file(key=DEFAULT_KEY, file_name=DEFAULT_FILE_NAME, start_path=None):
    """
    Search common locations for an env file and return the value for `key`.

    Locations searched (in order, de-duplicated): `start_path`, the current
    working directory, the home folder, and the `.envy_all` / `envy_all`
    folders within the home directory.
    """
    home = os.path.expanduser("~")
    directories = [start_path, os.getcwd(), home,
                   os.path.join(home, '.envy_all'), os.path.join(home, 'envy_all')]
    seen = []
    for directory in directories:
        if not directory or directory in seen:
            continue
        seen.append(directory)
        env_path = check_env_file(path=directory, file_name=file_name)
        if env_path:
            value = search_for_env_key(key=key, path=env_path)
            if value is not None:
                return value
    return None


def dotenv_load(path=None):
    """
    Load a dotenv file with python-dotenv if it exists and is a dotfile.

    Returns True if the file was loaded, otherwise False.
    """
    if path and os.path.isfile(path) and os.path.basename(path).startswith('.'):
        load_dotenv(path)
        return True
    return False


# Backwards-compatible alias.
safe_env_load = dotenv_load


def get_env_value(key=DEFAULT_KEY, path=None, file_name=DEFAULT_FILE_NAME):
    """
    Retrieve an environment value: load it from a dotenv `path` if given,
    otherwise search common locations for the `file_name` env file.
    """
    if dotenv_load(path):
        return os.getenv(key)
    return find_and_read_env_file(file_name=file_name, key=key, start_path=os.getcwd())

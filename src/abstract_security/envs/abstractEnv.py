from .imports import *
from .utils import *


class abstractEnv:
    """Resolve a key from a `.env` file across a set of candidate directories."""

    def __init__(self, key='MY_PASSWORD', file_name=None, path=None, deep_scan=False):
        self.re_initialize(key=key, file_name=file_name or '.env',
                           path=path or os.getcwd(), deep_scan=deep_scan)

    def re_initialize(self, key='MY_PASSWORD', file_name='.env', path=None, deep_scan=False):
        """
        Configure the lookup.

        Args:
            key: The key to search for in the .env file.
            file_name: The name of the .env file.
            path: A directory to search, or a direct path to an .env file.
            deep_scan: Allow fuzzy (partial) matching of the key.
        """
        self.key = key or DEFAULT_KEY
        self.file_name = file_name or DEFAULT_FILE_NAME
        self.deep_scan = deep_scan
        self.current_folder = os.getcwd()
        path = path or self.current_folder
        if os.path.isfile(path):
            self.file_name = os.path.basename(path)
            self.path = os.path.dirname(path)
        else:
            self.path = path
        self.start_path_env = os.path.join(self.path, self.file_name)
        self.home_folder = os.path.expanduser("~")
        self.envy_all = os.path.join(self.home_folder, '.envy_all')
        self.directories = self.get_directories()
        self.env_path = None
        self.env_value = self.find_and_read_env_file(
            key=self.key, file_name=self.file_name, path=self.path)

    def get_directories(self):
        """Return the de-duplicated list of existing directories to search."""
        directories = []
        for directory in [self.path, self.current_folder, self.home_folder, self.envy_all]:
            if os.path.isdir(directory) and directory not in directories:
                directories.append(directory)
        return directories

    def find_and_read_env_file(self, key=None, file_name=None, path=None, deep_scan=None):
        """Search the candidate directories and return the first matching value."""
        key = key or self.key
        file_name = file_name or self.file_name
        deep_scan = self.deep_scan if deep_scan is None else deep_scan
        for directory in self.directories:
            if not (directory and os.path.isdir(directory)):
                continue
            env_path = os.path.join(directory, file_name)
            if os.path.isfile(env_path):
                value = self.search_for_env_key(key=key, path=env_path, deep_scan=deep_scan)
                if value is not None:
                    self.env_path = env_path
                    return value
        return None

    def search_for_env_key(self, key=None, path=None, deep_scan=False):
        """
        Return the value of `key` from the .env file at `path`.

        With `deep_scan`, fall back to the best partial key match that covers at
        least half of the requested key.
        """
        key = key or self.key
        path = path or self.start_path_env
        if not path or not os.path.isfile(path):
            return None
        best_value, best_score = None, 0
        with open(path, "r") as f:
            for line in f:
                line_key, line_value = split_eq(line)
                if line_key == key:
                    return line_value
                if deep_scan and line_key:
                    matched = sum(len(part) for part in key.split('_') if part in line_key)
                    if key and matched / len(key) >= 0.5 and matched > best_score:
                        best_value, best_score = line_value, matched
        return best_value if deep_scan else None


AbstractEnv = abstractEnv

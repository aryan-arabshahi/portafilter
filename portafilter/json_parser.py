from typing import Any
from json import load as json_load


class JsonParser:

    _config_path = None
    _data = {}

    def __init__(self, config_path: str):
        """The init method

        Keyword Arguments:
            config_path (str) -- The JSON config path
        """
        self.load_config(config_path)

    def load_config(self, config_path: str = None) -> None:
        """Load the config file

        Keyword Arguments:
            config_path (str) -- The JSON config path (default None)
        """
        self._config_path = config_path

        self._data = self._read_json_file(self._config_path)

    @staticmethod
    def _read_json_file(file_path: str) -> dict:
        """Read the json file

        Arguments:
            file_path (str) -- The JSON file path
        """
        data = {}

        with open(file_path) as file:
            data = json_load(file)

        return data

    def get(self, key: str, default_value: Any = None) -> Any:
        """Get the variable from the loaded config

        Arguments:
            key (str) -- The specific key

        Keyword Arguments:
            default_value (Any) -- The default value (default None)
        """
        return self._walk_into_data(self._data, key) or default_value

    def _walk_into_data(self, data: Any, key: str, walk_depth: int = 0) -> Any:
        """Walk into the nested data

        Arguments:
            data (Any) -- The data source
            key (str) -- The nested key separated by dots

        Keyword Arguments:
            walk_depth (int) -- The current walking depth (default 0)

        Returns:
            Any
        """
        if walk_depth >= 10:
            raise Exception('The maximum walking depth is exceeded')

        walk_depth += 1
        splitted_key = key.split('.')
        target_key = splitted_key.pop(0)
        key_path = '.'.join(splitted_key)

        target_data = data.get(target_key, {})

        if splitted_key:

            return self._walk_into_data(target_data, key_path, walk_depth)

        return target_data

from os.path import join as join_path
from typing import Union, Dict
from portafilter.json_parser import JsonParser
from portafilter import __path__ as module_base_path


class Translate:

    def __init__(self, trans_file: str):
        """The initialize method

        Arguments:
            trans_file (str) -- The translate file path.
        """
        self._translate_map = JsonParser(trans_file)

    def get(self, key: str, attributes: Union[Dict, None] = None) -> str:
        """Get the translated key

        Arguments:
            key (str) -- The key

        Keyword Arguments:
            attributes (Union[Dict, None]) -- The string attributes to replace (default None)

        Returns:
            str
        """
        translated_string = self._translate_map.get(key, key)

        if attributes:
            for _attribute, _value in attributes.items():
                translated_string = translated_string.replace(f':{_attribute}', str(_value))

        return translated_string


class TransCollection:

    _instance = None

    def __init__(self):

        if TransCollection._instance is not None:
            raise Exception('The class is a singleton')

        else:
            TransCollection._instance = self

        self._data = {}

    @staticmethod
    def get_instance():
        if TransCollection._instance is None:
            TransCollection()

        return TransCollection._instance

    def get(self, key: str, attributes: Union[Dict, None] = None) -> str:
        """Get the translated key

        Arguments:
            key (str) -- The key

        Keyword Arguments:
            attributes (Union[Dict, None]) -- The string attributes to replace (default None)

        Returns:
            str
        """
        key = key.split('.')
        trans_file = key.pop(0)
        key = '.'.join(key)

        trans = self._get_trans(trans_file)

        if not trans:
            trans = self._load_trans(trans_file)

        return trans.get(key, attributes)

    def _get_trans(self, trans_file: str) -> Union[Translate, None]:
        """Get the translate instance

        Arguments:
            trans_file (str) -- The translate file name.

        Return:
            Union[Translate, None]
        """
        return self._data.get(trans_file)

    def _load_trans(self, trans_file: str) -> Translate:
        """Load the specified translate

        Arguments:
            trans_file (str) -- The translate file name.

        Return:
            Union[Translate, None]

        Raises:
            Exception -- The translate file name.
        """
        trans = Translate(join_path(module_base_path[0], 'languages', f'{trans_file}.json'))
        self._data[trans_file] = trans
        return trans

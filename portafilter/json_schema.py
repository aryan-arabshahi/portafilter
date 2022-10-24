from typing import Any, Tuple, List, Union, Set


class JsonSchema:

    def __init__(self, data: Union[dict, None] = None):
        """The initialize method.

        Arguments:
            data {Union[dict, None]} -- The data input (default: {None})
        """
        self._data = data

    def get_value_details(self, attribute: str, data: dict, default_value: Any = None) -> \
            Union[Tuple[Any, bool], List[Tuple[int, Tuple[Any, bool]]]]:
        """Get the specified attribute value details

        Arguments:
            attribute {str}
            data {dict}

        Keyword Arguments:
            default_value {Any}

        Returns:
            Union[Tuple[Any, bool], List[Tuple[int, Tuple[Any, bool]]]] -- The value and the existed flag or
            the list of the index and the tuple of the value and the existed flag.
        """
        try:
            _key = attribute.split('.')
            iteration = len(_key)
            _key_path = []

            if iteration > 1:
                result = None
                counter = 1

                key_exists = False
                for key_holder in _key:
                    _key_path.append(key_holder)

                    if isinstance(result, list):

                        if key_holder == '*':

                            if _key[-1] == '*':
                                result = self.get_value_details(f"{'.'.join([str(a) for a in _key_path[:-1]])}", data,
                                                                default_value=default_value)[0]
                                key_exists = True
                                break

                            list_result = []
                            list_index = 0
                            for list_item in result:
                                list_item_target_key = '.'.join(_key[counter:])
                                # Recursive
                                list_result.append(
                                    (list_index, self.get_value_details(list_item_target_key, list_item,
                                                                        default_value=default_value)))
                                list_index += 1

                            return list_result

                        else:
                            try:
                                parsed_partial_key = int(key_holder)

                                result = self.get_value_details(f"{'.'.join([str(a) for a in _key_path[:-1]])}", data,
                                                                default_value=default_value)[0][parsed_partial_key]
                                key_exists = True
                                break

                            except (ValueError, IndexError) as e:
                                # TODO:@@@@
                                # handle the not existed value
                                result = None
                                key_exists = False
                                pass

                    if counter == 1:
                        key_exists = JsonSchema._key_exists(key_holder, data)
                        result = data.get(key_holder, {})

                    elif counter < iteration:
                        key_exists = JsonSchema._key_exists(key_holder, result)
                        result = result.get(key_holder, {})

                    else:
                        key_exists = JsonSchema._key_exists(key_holder, result)
                        result = result.get(key_holder, default_value)

                    counter += 1

                return result, key_exists

            else:
                return data.get(_key[0], default_value), _key[0] in data

        except AttributeError as e:
            return default_value, False

    @staticmethod
    def _key_exists(key: str, data: Any) -> bool:
        """The key exists check

        Arguments:
            key {str}
            data {Any}

        Returns:
            bool
        """
        try:
            return key in data

        except Exception as e:
            return False

    def dot(self) -> dict:
        """Flat the dictionary with dot

        Returns:
            dict
        """
        result = {}
        self._dot_walk(self._data, result)
        return result

    def _dot_walk(self, data: Union[None, list, dict], result: dict, key_path: list = []) -> None:
        """Flat the dictionary with dot

        Keyword Arguments:
            data {Union[None, list, dict]} -- The data input (default: {None})
            key_path {list} -- The key path (default: {[]})

        Returns:
            dict
        """
        for key, value in data.items():
            key_path.append(key)

            if isinstance(value, dict):
                self._dot_walk(value, result, key_path)
                key_path.pop()

            elif isinstance(value, list):
                list_index = 0
                for list_item in value:
                    key_path.append(str(list_index))

                    if isinstance(list_item, list) or isinstance(list_item, dict):
                        self._dot_walk(list_item, result, key_path)

                    else:
                        result['.'.join(key_path)] = list_item

                    key_path.pop()

                    list_index += 1

                key_path.pop()

            else:
                result['.'.join(key_path)] = value
                key_path.pop()

from typing import Any, Tuple, List, Union, Set


class JsonSchema:

    def __init__(self, data: Union[dict, None] = None):
        """The initialize method.

        Arguments:
            data {Union[dict, None]} -- The data input (default: {None})
        """
        self._data = data

    def get_value_details(self, attribute: str, default_value: Any = None) -> \
            Union[Tuple[Any, bool], List[Tuple[int, Tuple[Any, bool]]]]:
        """Get the specified attribute value details

        Arguments:
            attribute {str}

        Keyword Arguments:
            default_value {Any}

        Returns:
            Union[Tuple[Any, bool], List[Tuple[int, Tuple[Any, bool]]]] -- The value and the existed flag or
            the list of the index and the tuple of the value and the existed flag.
        """
        return self._walk_into_data(attribute, self._data, default_value)

    def _walk_into_data(self, attribute: str, data: dict, default_value: Any = None) -> \
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

            if self.is_integer(_key[-1]) or _key[-1] == '*':
                _partial_key = _key.pop()
                if not _key:
                    _key = [_partial_key]
                else:
                    _key = ['.'.join(_key), _partial_key]

            iteration = len(_key)
            _key_path = []

            if iteration > 1:
                result = None
                counter = 1

                key_exists = False
                for key_holder in _key:

                    _key_path.append(key_holder)

                    if self.is_integer(key_holder):
                        _list_key = f"{'.'.join([str(a) for a in _key[:-1]])}"
                        if _list_key in data:
                            result = self._walk_into_data(
                                attribute.replace(_list_key, '').strip('.'),
                                data.get(_list_key),
                                default_value=default_value
                            )
                            key_exists = True
                            break

                    if isinstance(result, list):

                        if key_holder == '*':
                            _walk_into_list = True

                            if _key[-1] == '*':
                                _walk_into_list = False

                                result = self._walk_into_data(
                                    f"{'.'.join([str(a) for a in _key_path[:-1]])}",
                                    data,
                                    default_value=default_value
                                )[0]

                                if not isinstance(result, list):
                                    key_exists = True
                                    break

                            list_result = []
                            list_index = 0
                            for list_item in result:
                                list_item_target_key = '.'.join(_key[counter:])
                                # Recursive
                                list_result.append(
                                    (
                                        list_index,
                                        self._walk_into_data(
                                            list_item_target_key,
                                            list_item,
                                            default_value=default_value
                                        )
                                        if _walk_into_list else (list_item, True)
                                    )
                                )
                                list_index += 1

                            return list_result

                        else:
                            try:
                                parsed_partial_key = int(key_holder)

                                result = self._walk_into_data(
                                    f"{'.'.join([str(a) for a in _key_path[:-1]])}",
                                    data,
                                    default_value=default_value
                                )[0][parsed_partial_key]

                                key_exists = True
                                break

                            except (ValueError, IndexError) as e:
                                # TODO: handle the not existed value
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
                if self.is_integer(_key[0]) and isinstance(data, list):
                    return data[int(_key[0])]

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

    @staticmethod
    def is_integer(value: Any) -> bool:
        """The is integer check

        Arguments:
            value (Any)
        
        Returns:
            bool
        """
        try:
            int(value)
            return True

        except ValueError as e:
            return False

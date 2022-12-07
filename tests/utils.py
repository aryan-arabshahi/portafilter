from typing import Union, Any
from portafilter.json_schema import JsonSchema


class TestUtils:

    @staticmethod
    def assert_true(value: bool) -> None:
        """Assert true check

        Arguments:
            value {bool}

        Raises:
            AssertionError
        """
        assert value

    @staticmethod
    def assert_false(value: bool) -> None:
        """Assert false check

        Arguments:
            value {bool}

        Raises:
            AssertionError
        """
        assert not value

    @staticmethod
    def assert_json(data: dict, schema: Union[dict, str], value: Any = None) -> None:
        """Assert json

        Arguments:
            data {dict} -- The data input.
            schema {Union[dict, str]} -- The json schema.

        Keyword Arguments:
            value {Any} -- The value which is used for the json path mode (default: {None})

        Raises:
            AssertionError
            NotImplementedError
        """
        if isinstance(schema, str):
            assert JsonSchema(data).get_value_details(schema)[0] == value

        elif isinstance(schema, dict):
            for dict_key, dict_value in JsonSchema(schema).dot().items():
                assert JsonSchema(data).get_value_details(dict_key)[0] == dict_value

        else:
            raise NotImplementedError

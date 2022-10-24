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
            assert JsonSchema().get_value_details(schema, data)[0] == value

        elif isinstance(schema, dict):
            for dict_key, dict_value in JsonSchema(schema).dot().items():
                assert JsonSchema().get_value_details(dict_key, data)[0] == dict_value

        else:
            raise NotImplementedError

# self.assert_json_structure(
#     validator.errors(),
#     'name',
#     'asdasd'
# )

# self.assert_json_structure(
#     validator.errors(),
#     'name',
#     'asdasd'
# )

# ->assertJson([
#     'created' => true,
# ]);

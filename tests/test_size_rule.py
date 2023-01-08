from portafilter.json_schema import JsonSchema
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestSizeRule(BaseTest):

    def test_size_characters_fail(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'size:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.size.string', attributes={'attribute': 'name', 'size': 3})]
            }
        )

    def test_size_characters_success(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'size:4',
            }
        )

        self.assert_false(validator.fails())

    def test_size_characters_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'nullable|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_characters_nullable_success(self):
        validator = Validator(
            {
                'name': None,
            },
            {
                'name': 'nullable|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_integer_fail(self):
        validator = Validator(
            {
                'age': 4,
            },
            {
                'age': 'integer|size:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.size.numeric', attributes={'attribute': 'age', 'size': 3})]
            }
        )

    def test_size_integer_success(self):
        validator = Validator(
            {
                'age': 4,
            },
            {
                'age': 'integer|size:4',
            }
        )

        self.assert_false(validator.fails())

    def test_size_integer_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'integer|nullable|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_integer_nullable_success(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'integer|nullable|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|size:2',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.size.list', attributes={'attribute': 'coffee_menu', 'size': 2})]
            }
        )

    def test_size_list_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_list_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'list|nullable|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_list_nullable_success(self):
        validator = Validator(
            {
                'coffee_menu': None,
            },
            {
                'coffee_menu': 'list|nullable|size:3',
            }
        )

        self.assert_false(validator.fails())

    def test_size_list_fail_invalid_value_type(self):
        validator = Validator(
            {
                'coffee_menu': {'name': 'espresso'},
            },
            {
                'coffee_menu': 'size:2',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.size.string', attributes={'attribute': 'coffee_menu', 'size': 2})]
            }
        )

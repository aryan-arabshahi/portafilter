from portafilter.json_schema import JsonSchema
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestMaxRule(BaseTest):

    def test_max_characters_fail(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'max:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.max.string', attributes={'attribute': 'name', 'max': 3})]
            }
        )

    def test_max_characters_success(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'max:4',
            }
        )

        self.assert_false(validator.fails())

    def test_max_characters_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_characters_nullable_success(self):
        validator = Validator(
            {
                'name': None,
            },
            {
                'name': 'nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_integer_fail(self):
        validator = Validator(
            {
                'age': 4,
            },
            {
                'age': 'integer|max:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.max.numeric', attributes={'attribute': 'age', 'max': 3})]
            }
        )

    def test_max_integer_success(self):
        validator = Validator(
            {
                'age': 4,
            },
            {
                'age': 'integer|max:4',
            }
        )

        self.assert_false(validator.fails())

    def test_max_integer_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'integer|nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_integer_nullable_success(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'integer|nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|max:2',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.max.list', attributes={'attribute': 'coffee_menu', 'max': 2})]
            }
        )

    def test_max_list_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'list|nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_nullable_success(self):
        validator = Validator(
            {
                'coffee_menu': None,
            },
            {
                'coffee_menu': 'list|nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_fail_invalid_value_type(self):
        validator = Validator(
            {
                'coffee_menu': {'name': 'espresso'},
            },
            {
                'coffee_menu': 'max:2',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.max.string', attributes={'attribute': 'coffee_menu', 'max': 2})]
            }
        )

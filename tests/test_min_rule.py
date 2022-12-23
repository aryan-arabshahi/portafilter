from portafilter.json_schema import JsonSchema
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestMinRule(BaseTest):

    def test_min_characters_fail(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'min:5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.min.string', attributes={'attribute': 'name', 'min': 5})]
            }
        )

    def test_min_characters_success(self):
        validator = Validator(
            {
                'name': '12345',
            },
            {
                'name': 'min:5',
            }
        )

        self.assert_false(validator.fails())

    def test_min_characters_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_characters_nullable_success(self):
        validator = Validator(
            {
                'name': None,
            },
            {
                'name': 'nullable|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_integer_fail(self):
        validator = Validator(
            {
                'age': 4,
            },
            {
                'age': 'integer|min:5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.min.numeric', attributes={'attribute': 'age', 'min': 5})]
            }
        )

    def test_min_integer_success(self):
        validator = Validator(
            {
                'age': 5,
            },
            {
                'age': 'integer|min:5',
            }
        )

        self.assert_false(validator.fails())

    def test_min_integer_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'integer|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_integer_nullable_success(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'integer|nullable|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso'],
            },
            {
                'coffee_menu': 'list|min:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.min.list', attributes={'attribute': 'coffee_menu', 'min': 3})]
            }
        )

    def test_min_list_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_list_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'list|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_list_nullable_success(self):
        validator = Validator(
            {
                'coffee_menu': None,
            },
            {
                'coffee_menu': 'list|nullable|min:3',
            }
        )

        self.assert_false(validator.fails())

from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestIntegerRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'age': 10,
            },
            {
                'age': 'required|integer',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'required|integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.required', attributes={'attribute': 'age'})]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'required|integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                    trans('en.integer', attributes={'attribute': 'age'}),
                ]
            }
        )

    def test_required_with_zero_value_success(self):
        validator = Validator(
            {
                'age': 0,
            },
            {
                'age': 'required',
            }
        )

        self.assert_false(validator.fails())

    def test_non_integer_value_fail(self):
        validator = Validator(
            {
                'age': '10',
            },
            {
                'age': 'integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.integer', attributes={'attribute': 'age'})]
            }
        )

    def test_integer_value_success(self):
        validator = Validator(
            {
                'age': 10,
            },
            {
                'age': 'integer',
            }
        )

        self.assert_false(validator.fails())

    def test_required_integer_fail_empty_string(self):
        validator = Validator(
            {
                'age': '',
            },
            {
                'age': 'required|integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                    trans('en.integer', attributes={'attribute': 'age'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'integer|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'age': None
            },
            {
                'age': 'integer|nullable',
            }
        )

        self.assert_false(validator.fails())

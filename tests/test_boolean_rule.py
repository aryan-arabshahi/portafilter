from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestBooleanRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'is_verified': True,
            },
            {
                'is_verified': 'required|boolean',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'is_verified': 'required|boolean',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'is_verified': [trans('en.required', attributes={'attribute': 'is_verified'})]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'is_verified': None,
            },
            {
                'is_verified': 'required|boolean',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'is_verified': [
                    trans('en.required', attributes={'attribute': 'is_verified'}),
                    trans('en.boolean', attributes={'attribute': 'is_verified'}),
                ]
            }
        )

    def test_non_boolean_value_fail(self):
        validator = Validator(
            {
                'is_verified': '10',
            },
            {
                'is_verified': 'boolean',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'is_verified': [trans('en.boolean', attributes={'attribute': 'is_verified'})]
            }
        )

    def test_boolean_value_success(self):
        validator = Validator(
            {
                'is_verified': False,
            },
            {
                'is_verified': 'boolean',
            }
        )

        self.assert_false(validator.fails())

    def test_required_boolean_fail_empty_string(self):
        validator = Validator(
            {
                'is_verified': '',
            },
            {
                'is_verified': 'required|boolean',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'is_verified': [
                    trans('en.required', attributes={'attribute': 'is_verified'}),
                    trans('en.boolean', attributes={'attribute': 'is_verified'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'is_verified': 'boolean|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'is_verified': None
            },
            {
                'is_verified': 'boolean|nullable',
            }
        )

        self.assert_false(validator.fails())

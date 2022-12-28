from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestSameRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'password': 'espresso',
                'password_confirmation': 'espresso',
            },
            {
                'password': 'required|same:password_confirmation',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
                'password_confirmation': 'espresso',
            },
            {
                'password': 'required|same:password_confirmation',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'password': [
                    trans('en.required', attributes={'attribute': 'password'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'password': None,
                'password_confirmation': 'espresso',
            },
            {
                'password': 'required|same:password_confirmation',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'password': [
                    trans('en.required', attributes={'attribute': 'password'}),
                ]
            }
        )

    def test_non_same_value_fail(self):
        validator = Validator(
            {
                'password': 'espresso',
                'password_confirmation': 'mocha',
            },
            {
                'password': 'same:password_confirmation',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'password': [
                    trans('en.same', attributes={'attribute': 'password', 'other': 'password_confirmation'}),
                ]
            }
        )

    def test_same_value_success(self):
        validator = Validator(
            {
                'password': 'espresso',
                'password_confirmation': 'espresso',
            },
            {
                'password': 'same:password_confirmation',
            }
        )

        self.assert_false(validator.fails())

    def test_required_same_fail_empty_string(self):
        validator = Validator(
            {
                'password': '',
                'password_confirmation': '',
            },
            {
                'password': 'required|same:password_confirmation',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'password': [
                    trans('en.required', attributes={'attribute': 'password'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
                'password_confirmation': '',
            },
            {
                'password': 'nullable|same:password_confirmation',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'password': None,
                'password_confirmation': 'espresso',
            },
            {
                'password': 'nullable|same:password_confirmation',
            }
        )

        self.assert_false(validator.fails())

    def test_same_fail_invalid_value_type(self):
        validator = Validator(
            {
                'current_password': {'name': 'espresso'},
                'new_password': 'espresso',
            },
            {
                'current_password': 'required|same:new_password',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'current_password': [
                    trans('en.same', attributes={'attribute': 'current_password', 'other': 'new_password'}),
                ]
            }
        )

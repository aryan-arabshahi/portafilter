from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestDifferentRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'current_password': 'espresso',
                'new_password': 'cortado',
            },
            {
                'current_password': 'required|different:new_password',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
                'new_password': 'espresso',
            },
            {
                'current_password': 'required|different:new_password',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'current_password': [
                    trans('en.required', attributes={'attribute': 'current_password'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'current_password': None,
                'new_password': 'espresso',
            },
            {
                'current_password': 'required|different:new_password',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'current_password': [
                    trans('en.required', attributes={'attribute': 'current_password'}),
                ]
            }
        )

    def test_non_different_value_fail(self):
        validator = Validator(
            {
                'current_password': 'espresso',
                'new_password': 'espresso',
            },
            {
                'current_password': 'different:new_password',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'current_password': [
                    trans('en.different', attributes={'attribute': 'current_password', 'other': 'new_password'}),
                ]
            }
        )

    def test_different_value_success(self):
        validator = Validator(
            {
                'current_password': 'espresso',
                'new_password': 'cortado',
            },
            {
                'current_password': 'different:new_password',
            }
        )

        self.assert_false(validator.fails())

    def test_required_different_fail_empty_string(self):
        validator = Validator(
            {
                'current_password': '',
                'new_password': '',
            },
            {
                'current_password': 'required|different:new_password',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'current_password': [
                    trans('en.required', attributes={'attribute': 'current_password'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
                'new_password': '',
            },
            {
                'current_password': 'nullable|different:new_password',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'current_password': None,
                'new_password': 'espresso',
            },
            {
                'current_password': 'nullable|different:new_password',
            }
        )

        self.assert_false(validator.fails())

    def test_different_fail_invalid_value_type(self):
        validator = Validator(
            {
                'current_password': {'name': 'espresso'},
                'new_password': {'name': 'espresso'},
            },
            {
                'current_password': 'required|different:new_password',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'current_password': [
                    trans('en.different', attributes={'attribute': 'current_password', 'other': 'new_password'}),
                ]
            }
        )

from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestEmailRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'email': 'mocha@codewithcoffee.dev',
            },
            {
                'email': 'required|email',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'email': 'required|email',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.required', attributes={'attribute': 'email'}),
                    trans('en.email', attributes={'attribute': 'email'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'email': None,
            },
            {
                'email': 'required|email',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.required', attributes={'attribute': 'email'}),
                    trans('en.email', attributes={'attribute': 'email'}),
                ]
            }
        )

    def test_non_email_value_fail(self):
        validator = Validator(
            {
                'email': '10',
            },
            {
                'email': 'email',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [trans('en.email', attributes={'attribute': 'email'})]
            }
        )

    def test_email_value_success(self):
        validator = Validator(
            {
                'email': 'mocha@codewithcoffee.dev',
            },
            {
                'email': 'email',
            }
        )

        self.assert_false(validator.fails())

    def test_required_email_fail_empty_string(self):
        validator = Validator(
            {
                'email': '',
            },
            {
                'email': 'required|email',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.required', attributes={'attribute': 'email'}),
                    trans('en.email', attributes={'attribute': 'email'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'email': 'email|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'email': None
            },
            {
                'email': 'email|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_email_fail_invalid_value_type(self):
        validator = Validator(
            {
                'email': {'name': 'espresso'},
            },
            {
                'email': 'required|email',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.email', attributes={'attribute': 'email'}),
                ]
            }
        )

from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestNotInRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'coffee': 'doppio',
            },
            {
                'coffee': 'required|not_in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee': 'required|not_in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.required', attributes={'attribute': 'coffee'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'coffee': None,
            },
            {
                'coffee': 'required|not_in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.required', attributes={'attribute': 'coffee'}),
                ]
            }
        )

    def test_non_not_in_value_fail(self):
        validator = Validator(
            {
                'coffee': 'mocha',
            },
            {
                'coffee': 'not_in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [trans('en.not_in', attributes={'attribute': 'coffee'})]
            }
        )

    def test_not_in_value_success(self):
        validator = Validator(
            {
                'coffee': 'doppio',
            },
            {
                'coffee': 'not_in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_required_not_in_fail_empty_string(self):
        validator = Validator(
            {
                'coffee': '',
            },
            {
                'coffee': 'required|not_in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.required', attributes={'attribute': 'coffee'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee': 'nullable|not_in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'coffee': None
            },
            {
                'coffee': 'nullable|not_in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

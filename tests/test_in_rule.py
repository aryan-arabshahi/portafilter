from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestInRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'coffee': 'espresso',
            },
            {
                'coffee': 'required|in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_in_with_integer_value_success(self):
        validator = Validator(
            {
                'coffee': 10,
            },
            {
                'coffee': 'integer|in:0,10,20',
            }
        )

        self.assert_false(validator.fails())

    def test_in_with_float_value_success(self):
        validator = Validator(
            {
                'coffee': 10.2,
            },
            {
                'coffee': 'numeric|in:0,10,20,10.2',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee': 'required|in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.required', attributes={'attribute': 'coffee'}),
                    trans('en.in', attributes={'attribute': 'coffee'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'coffee': None,
            },
            {
                'coffee': 'required|in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.required', attributes={'attribute': 'coffee'}),
                    trans('en.in', attributes={'attribute': 'coffee'}),
                ]
            }
        )

    def test_non_in_value_fail(self):
        validator = Validator(
            {
                'coffee': 'tea',
            },
            {
                'coffee': 'in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [trans('en.in', attributes={'attribute': 'coffee'})]
            }
        )

    def test_in_value_success(self):
        validator = Validator(
            {
                'coffee': 'mocha',
            },
            {
                'coffee': 'in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_required_in_fail_empty_string(self):
        validator = Validator(
            {
                'coffee': '',
            },
            {
                'coffee': 'required|in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.required', attributes={'attribute': 'coffee'}),
                    trans('en.in', attributes={'attribute': 'coffee'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee': 'nullable|in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'coffee': None
            },
            {
                'coffee': 'nullable|in:espresso,latte,mocha',
            }
        )

        self.assert_false(validator.fails())

    def test_in_fail_invalid_value_type(self):
        validator = Validator(
            {
                'coffee': {'name': 'espresso'},
            },
            {
                'coffee': 'required|in:espresso,latte,mocha',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.in', attributes={'attribute': 'coffee'}),
                ]
            }
        )

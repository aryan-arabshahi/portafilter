from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestStringRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'name': 'espresso',
            },
            {
                'name': 'required',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.required', attributes={'attribute': 'name'})]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'name': None,
            },
            {
                'name': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.required', attributes={'attribute': 'name'})]
            }
        )

    def test_non_string_value_fail(self):
        validator = Validator(
            {
                'name': 10,
            },
            {
                'name': 'string',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.string', attributes={'attribute': 'name'})]
            }
        )

    def test_string_value_success(self):
        validator = Validator(
            {
                'name': 'espresso',
            },
            {
                'name': 'string',
            }
        )

        self.assert_false(validator.fails())

    def test_required_fail_empty_string(self):
        validator = Validator(
            {
                'name': '',
            },
            {
                'name': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': [trans('en.required', attributes={'attribute': 'name'})]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'name': None
            },
            {
                'name': 'nullable',
            }
        )

        self.assert_false(validator.fails())

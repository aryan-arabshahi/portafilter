from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestDateRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|date',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'date': 'required|date',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [trans('en.required', attributes={'attribute': 'date'})]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'date': None,
            },
            {
                'date': 'required|date',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.required', attributes={'attribute': 'date'}),
                    trans('en.date', attributes={'attribute': 'date'}),
                ]
            }
        )

    def test_non_date_value_fail(self):
        validator = Validator(
            {
                'date': ['espresso'],
            },
            {
                'date': 'date',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [trans('en.date', attributes={'attribute': 'date'})]
            }
        )

    def test_date_value_success(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'date',
            }
        )

        self.assert_false(validator.fails())

    def test_required_date_fail_empty_string(self):
        validator = Validator(
            {
                'date': '',
            },
            {
                'date': 'required|date',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.required', attributes={'attribute': 'date'}),
                    trans('en.date', attributes={'attribute': 'date'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'date': 'date|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'date': None
            },
            {
                'date': 'date|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_date_format_success(self):
        validator = Validator(
            {
                'date': '2022-12-23 13:22:05',
            },
            {
                'date': 'date:%Y-%m-%d %H:%M:%S',
            }
        )

        self.assert_false(validator.fails())

    def test_date_format_fail(self):
        validator = Validator(
            {
                'date': '2022-12-23 13:22',
            },
            {
                'date': 'date:%Y-%m-%d %H:%M:%S',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [trans('en.date_format', attributes={'attribute': 'date', 'format': '%Y-%m-%d %H:%M:%S'})]
            }
        )

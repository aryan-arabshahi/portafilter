from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestRequiredRule(BaseTest):

    def test_required_zero_numeric_value_success(self):
        validator = Validator(
            {
                'age': 0,
            },
            {
                'age': 'required',
            }
        )

        self.assert_false(validator.fails())

    def test_required_false_boolean_value_success(self):
        validator = Validator(
            {
                'age': False,
            },
            {
                'age': 'required',
            }
        )

        self.assert_false(validator.fails())

    def test_required_none_value_fail(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                ]
            }
        )

    def test_required_empty_list_fail(self):
        validator = Validator(
            {
                'age': [],
            },
            {
                'age': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                ]
            }
        )

    def test_required_empty_dict_fail(self):
        validator = Validator(
            {
                'age': {},
            },
            {
                'age': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                ]
            }
        )

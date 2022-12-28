from portafilter.sandglass import Sandglass
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestBeforeOrEqualRule(BaseTest):

    def test_before_or_equal_with_date_success(self):
        validator = Validator(
            {
                'date': '2022-12-24',
            },
            {
                'date': 'required|before_or_equal:2022-12-24',
            }
        )

        self.assert_false(validator.fails())

    def test_before_or_equal_with_date_fail(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|before_or_equal:2022-12-22',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.before_or_equal', attributes={'attribute': 'date', 'date': '2022-12-22'})
                ],
            }
        )

    def test_before_or_equal_with_special_key_success(self):
        validator = Validator(
            {
                'date': Sandglass.now().to_string('%Y-%m-%d'),
            },
            {
                'date': 'required|before_or_equal:tomorrow',
            }
        )

        self.assert_false(validator.fails())

    def test_before_or_equal_with_special_key_fail(self):
        validator = Validator(
            {
                'date': Sandglass.now().to_string('%Y-%m-%d'),
            },
            {
                'date': 'required|before_or_equal:yesterday',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.before_or_equal', attributes={'attribute': 'date', 'date': 'yesterday'})
                ],
            }
        )

    def test_before_or_equal_with_special_key_fail_invalid_value_type(self):
        validator = Validator(
            {
                'date': {'name': 'espresso'},
            },
            {
                'date': 'required|before_or_equal:yesterday',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.before_or_equal', attributes={'attribute': 'date', 'date': 'yesterday'})
                ],
            }
        )

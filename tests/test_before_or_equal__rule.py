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
                'date': 'required|before_or_equal:2022-12-23',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.before_or_equal', attributes={'attribute': 'date', 'date': '2022-12-23'})
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
                'date': 'required|before_or_equal:tomorrow',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.before_or_equal', attributes={'attribute': 'date', 'date': Sandglass.yesterday()
                          .to_string('%Y-%m-%d')})
                ],
            }
        )

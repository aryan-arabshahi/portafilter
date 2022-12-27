from portafilter.sandglass import Sandglass
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestAfterOrEqualRule(BaseTest):

    def test_after_or_equal_with_date_success(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|after_or_equal:2022-12-23',
            }
        )

        self.assert_false(validator.fails())

    def test_after_or_equal_with_date_fail(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|after_or_equal:2022-12-22',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.after_or_equal', attributes={'attribute': 'date', 'date': '2022-12-22'})
                ],
            }
        )

    def test_after_or_equal_with_special_key_success(self):
        validator = Validator(
            {
                'date': Sandglass.now().to_string('%Y-%m-%d'),
            },
            {
                'date': 'required|after_or_equal:today',
            }
        )

        self.assert_false(validator.fails())

    def test_after_or_equal_with_special_key_fail(self):
        validator = Validator(
            {
                'date': Sandglass.now().to_string('%Y-%m-%d'),
            },
            {
                'date': 'required|after_or_equal:yesterday',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.after_or_equal', attributes={'attribute': 'date', 'date': Sandglass.yesterday()
                          .to_string('%Y-%m-%d')})
                ],
            }
        )

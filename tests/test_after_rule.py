from portafilter.sandglass import Sandglass
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestAfterRule(BaseTest):

    def test_after_with_date_success(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|after:2022-12-22',
            }
        )

        self.assert_false(validator.fails())

    def test_after_with_date_fail(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|after:2022-12-23',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.after', attributes={'attribute': 'date', 'date': '2022-12-23'})
                ],
            }
        )

    def test_after_with_special_key_success(self):
        validator = Validator(
            {
                'date': Sandglass.now().to_string('%Y-%m-%d'),
            },
            {
                'date': 'required|after:yesterday',
            }
        )

        self.assert_false(validator.fails())

    def test_after_with_special_key_fail(self):
        validator = Validator(
            {
                'date': Sandglass.now().to_string('%Y-%m-%d'),
            },
            {
                'date': 'required|after:tomorrow',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.after', attributes={'attribute': 'date', 'date': 'tomorrow'})
                ],
            }
        )

from tests import BaseTest
from portafilter import Validator


class TestStringRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'name': self.faker.name(),
            },
            {
                'name': 'required',
            }
        )

        self.assert_false(validator.fails())

    def test_required_failed(self):
        validator = Validator(
            {
                'invalid_key_name': None,
            },
            {
                'name': 'required',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': ['The name field is required.']
            }
        )

    def test_required_failed_none_value(self):
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
                'name': ['The name field is required.']
            }
        )

    def test_required_failed_empty_string(self):
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
                'name': ['The name field is required.']
            }
        )


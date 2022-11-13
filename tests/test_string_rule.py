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
                'name': ['The name field is required.']
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
                'name': ['The name field is required.']
            }
        )

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
                'name': ['The name field is required.']
            }
        )

    def test_min_characters_fail(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'min:5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': ['The name must be at least 5 characters.']
            }
        )

    def test_min_characters_success(self):
        validator = Validator(
            {
                'name': '12345',
            },
            {
                'name': 'min:5',
            }
        )

        self.assert_false(validator.fails())

    def test_max_characters_fail(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'max:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'name': ['The name may not be greater than 3 characters.']
            }
        )

    def test_max_characters_success(self):
        validator = Validator(
            {
                'name': '1234',
            },
            {
                'name': 'max:4',
            }
        )

        self.assert_false(validator.fails())

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

    def test_min_characters_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_characters_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'name': 'nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_min_characters_nullable_success(self):
        validator = Validator(
            {
                'name': None,
            },
            {
                'name': 'nullable|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_characters_nullable_success(self):
        validator = Validator(
            {
                'name': None,
            },
            {
                'name': 'nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

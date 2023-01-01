from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestNumericRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'age': 10.5,
            },
            {
                'age': 'required|numeric',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'required|numeric',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.required', attributes={'attribute': 'age'})]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'required|numeric',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                    trans('en.numeric', attributes={'attribute': 'age'}),
                ]
            }
        )

    def test_required_with_zero_value_success(self):
        validator = Validator(
            {
                'age': 0,
            },
            {
                'age': 'required|numeric',
            }
        )

        self.assert_false(validator.fails())

    def test_non_numeric_value_fail(self):
        validator = Validator(
            {
                'age': '10',
            },
            {
                'age': 'numeric',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.numeric', attributes={'attribute': 'age'})]
            }
        )

    def test_numeric_value_success(self):
        validator = Validator(
            {
                'age': 10,
            },
            {
                'age': 'numeric',
            }
        )

        self.assert_false(validator.fails())

    def test_required_numeric_fail_empty_string(self):
        validator = Validator(
            {
                'age': '',
            },
            {
                'age': 'required|numeric',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.required', attributes={'attribute': 'age'}),
                    trans('en.numeric', attributes={'attribute': 'age'}),
                ]
            }
        )

    def test_min_numeric_fail(self):
        validator = Validator(
            {
                'age': 4.9,
            },
            {
                'age': 'numeric|min:5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.min.numeric', attributes={'attribute': 'age', 'min': 5})]
            }
        )

    def test_min_numeric_success(self):
        validator = Validator(
            {
                'age': 5,
            },
            {
                'age': 'numeric|min:5',
            }
        )

        self.assert_false(validator.fails())

    def test_max_numeric_fail(self):
        validator = Validator(
            {
                'age': 3.3,
            },
            {
                'age': 'numeric|max:3.2',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [trans('en.max.numeric', attributes={'attribute': 'age', 'max': 3.2})]
            }
        )

    def test_max_numeric_success(self):
        validator = Validator(
            {
                'age': 4,
            },
            {
                'age': 'numeric|max:4',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'numeric|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'age': None
            },
            {
                'age': 'numeric|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_min_numeric_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'numeric|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_numeric_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'age': 'numeric|nullable|max:3',
            }
        )
    
        self.assert_false(validator.fails())

    def test_min_numeric_nullable_success(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'numeric|nullable|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_numeric_nullable_success(self):
        validator = Validator(
            {
                'age': None,
            },
            {
                'age': 'numeric|nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_numeric_fail_invalid_value_type(self):
        validator = Validator(
            {
                'age': {'name': 'espresso'},
            },
            {
                'age': 'required|numeric',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': [
                    trans('en.numeric', attributes={'attribute': 'age'}),
                ]
            }
        )

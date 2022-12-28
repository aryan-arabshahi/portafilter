from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestStartsWithRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'choice': 'Coffee: Lungo',
            },
            {
                'choice': 'required|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_false(validator.fails())

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'choice': 'required|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'choice': [
                    trans('en.required', attributes={'attribute': 'choice'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'choice': None,
            },
            {
                'choice': 'required|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'choice': [
                    trans('en.required', attributes={'attribute': 'choice'}),
                ]
            }
        )

    def test_non_starts_with_value_fail(self):
        validator = Validator(
            {
                'choice': 'Espresso coffee',
            },
            {
                'choice': 'starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'choice': [
                    trans('en.starts_with', attributes={'attribute': 'choice', 'values': 'latte, coffee, Coffee'}),
                ]
            }
        )

    def test_starts_with_value_success(self):
        validator = Validator(
            {
                'choice': 'Espresso coffee',
            },
            {
                'choice': 'starts_with:Espress,latte,coffee,Coffee',
            }
        )

        self.assert_false(validator.fails())

    def test_required_starts_with_fail_empty_string(self):
        validator = Validator(
            {
                'choice': '',
            },
            {
                'choice': 'required|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'choice': [
                    trans('en.required', attributes={'attribute': 'choice'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'choice': 'nullable|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'choice': None,
            },
            {
                'choice': 'nullable|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_false(validator.fails())

    def test_starts_with_fail_invalid_value_type(self):
        validator = Validator(
            {
                'choice': {'name': 'espresso'},
            },
            {
                'choice': 'required|starts_with:latte,coffee,Coffee',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'choice': [
                    trans('en.starts_with', attributes={'attribute': 'choice', 'values': 'latte, coffee, Coffee'}),
                ]
            }
        )

from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestContainsOneOfRule(BaseTest):

    def test_required_string_contains_one_of_success(self):
        validator = Validator(
            {
                'ingredients': 'The main ingredients are robusta and water and a little microfoam.',
            },
            {
                'ingredients': 'required|contains_one_of:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_list_contains_one_of_success(self):
        validator = Validator(
            {
                'ingredients': ['water', 'microfoam', 'robusta'],
            },
            {
                'ingredients': 'required|contains_one_of:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_dict_contains_one_of_success(self):
        validator = Validator(
            {
                'coffee': {'id': 1, 'name': 'espresso'},
            },
            {
                'coffee': 'required|contains_one_of:id,name',
            }
        )

        self.assert_false(validator.fails())

    def test_string_contains_one_of_fail(self):
        validator = Validator(
            {
                'ingredients': 'The main ingredients are robusta and water and a little microfoam.',
            },
            {
                'ingredients': 'contains_one_of:milk,chocolate',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains_one_of', attributes={'attribute': 'ingredients', 'values': 'milk, chocolate'}),
                ]
            }
        )

    def test_list_contains_one_of_fail(self):
        validator = Validator(
            {
                'ingredients': ['water', 'microfoam', 'robusta'],
            },
            {
                'ingredients': 'contains_one_of:milk,chocolate',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains_one_of', attributes={'attribute': 'ingredients', 'values': 'milk, chocolate'}),
                ]
            }
        )

    def test_dict_contains_one_of_fail(self):
        validator = Validator(
            {
                'coffee': {'id': 1, 'name': 'espresso'},
            },
            {
                'coffee': 'contains_one_of:price,popular',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.contains_one_of', attributes={'attribute': 'coffee', 'values': 'price, popular'}),
                ]
            }
        )

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'ingredients': 'required|contains_one_of:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.required', attributes={'attribute': 'ingredients'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'ingredients': None,
            },
            {
                'ingredients': 'required|contains_one_of:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.required', attributes={'attribute': 'ingredients'}),
                ]
            }
        )

    def test_non_contains_one_of_value_fail(self):
        validator = Validator(
            {
                'ingredients': 'Espresso coffee',
            },
            {
                'ingredients': 'contains_one_of:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains_one_of', attributes={'attribute': 'ingredients', 'values': 'water, microfoam'}),
                ]
            }
        )

    def test_required_contains_one_of_fail_empty_string(self):
        validator = Validator(
            {
                'ingredients': '',
            },
            {
                'ingredients': 'required|contains_one_of:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.required', attributes={'attribute': 'ingredients'}),
                ]
            }
        )

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'ingredients': 'nullable|contains_one_of:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'ingredients': None,
            },
            {
                'ingredients': 'nullable|contains_one_of:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_contains_one_of_fail_invalid_value_type(self):
        validator = Validator(
            {
                'ingredients': {'name': 'espresso'},
            },
            {
                'ingredients': 'required|contains_one_of:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains_one_of', attributes={'attribute': 'ingredients', 'values': 'water, microfoam'}),
                ]
            }
        )

    def test_contains_one_of_success_only_one_of_values(self):
        validator = Validator(
            {
                'ingredients': 'The main ingredients are robusta and water and a little microfoam.',
            },
            {
                'ingredients': 'required|contains_one_of:water,chocolate',
            }
        )

        self.assert_false(validator.fails())

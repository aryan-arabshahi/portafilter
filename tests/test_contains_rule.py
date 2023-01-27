from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestContainsRule(BaseTest):

    def test_required_string_contains_success(self):
        validator = Validator(
            {
                'ingredients': 'The main ingredients are robusta and water and a little microfoam.',
            },
            {
                'ingredients': 'required|contains:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_list_contains_success(self):
        validator = Validator(
            {
                'ingredients': ['water', 'microfoam', 'robusta'],
            },
            {
                'ingredients': 'required|contains:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_dict_contains_success(self):
        validator = Validator(
            {
                'coffee': {'id': 1, 'name': 'espresso'},
            },
            {
                'coffee': 'required|contains:id,name',
            }
        )

        self.assert_false(validator.fails())

    def test_string_contains_fail(self):
        validator = Validator(
            {
                'ingredients': 'The main ingredients are robusta and water and a little microfoam.',
            },
            {
                'ingredients': 'contains:water,microfoam,roasted',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains', attributes={'attribute': 'ingredients', 'values': 'water, microfoam, '
                                                                                           'roasted'}),
                ]
            }
        )

    def test_list_contains_fail(self):
        validator = Validator(
            {
                'ingredients': ['water', 'microfoam', 'robusta'],
            },
            {
                'ingredients': 'contains:water,microfoam,roasted',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains', attributes={'attribute': 'ingredients', 'values': 'water, microfoam, '
                                                                                           'roasted'}),
                ]
            }
        )

    def test_dict_contains_fail(self):
        validator = Validator(
            {
                'coffee': {'id': 1, 'name': 'espresso'},
            },
            {
                'coffee': 'contains:id,name,type',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.contains', attributes={'attribute': 'coffee', 'values': 'id, name, type'}),
                ]
            }
        )

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'ingredients': 'required|contains:water,microfoam',
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
                'ingredients': 'required|contains:water,microfoam',
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

    def test_non_contains_value_fail(self):
        validator = Validator(
            {
                'ingredients': 'Espresso coffee',
            },
            {
                'ingredients': 'contains:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains', attributes={'attribute': 'ingredients', 'values': 'water, microfoam'}),
                ]
            }
        )

    def test_required_contains_fail_empty_string(self):
        validator = Validator(
            {
                'ingredients': '',
            },
            {
                'ingredients': 'required|contains:water,microfoam',
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
                'ingredients': 'nullable|contains:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'ingredients': None,
            },
            {
                'ingredients': 'nullable|contains:water,microfoam',
            }
        )

        self.assert_false(validator.fails())

    def test_contains_fail_invalid_value_type(self):
        validator = Validator(
            {
                'ingredients': {'name': 'espresso'},
            },
            {
                'ingredients': 'required|contains:water,microfoam',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.contains', attributes={'attribute': 'ingredients', 'values': 'water, microfoam'}),
                ]
            }
        )

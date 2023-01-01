from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestBetweenRule(BaseTest):

    def test_between_integer_success(self):
        validator = Validator(
            {
                'price': 10,
            },
            {
                'price': 'integer|between:8,12',
            }
        )

        self.assert_false(validator.fails())

    def test_between_integer_fail(self):
        validator = Validator(
            {
                'price': 20,
            },
            {
                'price': 'integer|between:8,12',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'price': [
                    trans('en.between.numeric', attributes={'attribute': 'price', 'min': 8, 'max': 12})
                ],
            }
        )

    def test_between_float_success(self):
        validator = Validator(
            {
                'price': 10.2,
            },
            {
                'price': 'numeric|between:10.1,10.5',
            }
        )

        self.assert_false(validator.fails())

    def test_between_float_fail(self):
        validator = Validator(
            {
                'price': 10.05,
            },
            {
                'price': 'numeric|between:10.1,10.5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'price': [
                    trans('en.between.numeric', attributes={'attribute': 'price', 'min': 10.1, 'max': 10.5})
                ],
            }
        )

    def test_between_string_success(self):
        validator = Validator(
            {
                'coffee': 'espresso',
            },
            {
                'coffee': 'between:3,8',
            }
        )

        self.assert_false(validator.fails())

    def test_between_string_fail(self):
        validator = Validator(
            {
                'coffee': 'espresso',
            },
            {
                'coffee': 'between:3,5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee': [
                    trans('en.between.string', attributes={'attribute': 'coffee', 'min': 3, 'max': 5})
                ],
            }
        )

    def test_between_list_success(self):
        validator = Validator(
            {
                'ingredients': ['robusta', 'microfoam', 'chocolate'],
            },
            {
                'ingredients': 'list|between:3,5',
            }
        )

        self.assert_false(validator.fails())

    def test_between_list_fail(self):
        validator = Validator(
            {
                'ingredients': ['robusta', 'microfoam'],
            },
            {
                'ingredients': 'list|between:3,5',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'ingredients': [
                    trans('en.between.list', attributes={'attribute': 'ingredients', 'min': 3, 'max': 5})
                ],
            }
        )

    def test_between_date_success(self):
        validator = Validator(
            {
                'date': '2023-01-02',
            },
            {
                'date': 'date|between:2023-01-01,2023-01-05',
            }
        )

        self.assert_false(validator.fails())

    def test_between_date_fail(self):
        validator = Validator(
            {
                'date': '2023-01-20',
            },
            {
                'date': 'date|between:2023-01-01,2023-01-05',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'date': [
                    trans('en.between.date', attributes={'attribute': 'date', 'min': '2023-01-01', 'max': '2023-01-05'})
                ],
            }
        )

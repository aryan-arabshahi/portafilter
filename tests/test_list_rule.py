from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestListRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso'],
            },
            {
                'coffee_menu': 'required|list',
            }
        )

        self.assert_false(validator.fails())

    def test_required_with_empty_list_success(self):
        validator = Validator(
            {
                'coffee_menu': [],
            },
            {
                'coffee_menu': 'required|list',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.required', attributes={'attribute': 'coffee_menu'})]
            }
        )

    def test_required_missing_key_fail(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'required|list',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [
                    trans('en.required', attributes={'attribute': 'coffee_menu'}),
                    trans('en.list', attributes={'attribute': 'coffee_menu'}),
                ]
            }
        )

    def test_required_fail_none_value(self):
        validator = Validator(
            {
                'coffee_menu': None,
            },
            {
                'coffee_menu': 'required|list',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [
                    trans('en.required', attributes={'attribute': 'coffee_menu'}),
                    trans('en.list', attributes={'attribute': 'coffee_menu'}),
                ]
            }
        )

    def test_non_list_value_fail(self):
        validator = Validator(
            {
                'coffee_menu': '10',
            },
            {
                'coffee_menu': 'list',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.list', attributes={'attribute': 'coffee_menu'})]
            }
        )

    def test_list_value_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso'],
            },
            {
                'coffee_menu': 'list',
            }
        )

        self.assert_false(validator.fails())

    def test_empty_list_value_success(self):
        validator = Validator(
            {
                'coffee_menu': [],
            },
            {
                'coffee_menu': 'list',
            }
        )

        self.assert_false(validator.fails())

    def test_required_list_fail_empty_list(self):
        validator = Validator(
            {
                'coffee_menu': [],
            },
            {
                'coffee_menu': 'required|list',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.required', attributes={'attribute': 'coffee_menu'})]
            }
        )

    def test_required_list_fail_empty_string(self):
        validator = Validator(
            {
                'coffee_menu': '',
            },
            {
                'coffee_menu': 'required|list',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [
                    trans('en.required', attributes={'attribute': 'coffee_menu'}),
                    trans('en.list', attributes={'attribute': 'coffee_menu'}),
                ]
            }
        )

    def test_min_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso'],
            },
            {
                'coffee_menu': 'list|min:3',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.min.list', attributes={'attribute': 'coffee_menu', 'min': 3})]
            }
        )

    def test_min_list_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|max:2',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.max.list', attributes={'attribute': 'coffee_menu', 'max': 2})]
            }
        )

    def test_max_list_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 'latte', 'mocha'],
            },
            {
                'coffee_menu': 'list|max:3',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'list|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_nullable_success(self):
        validator = Validator(
            {
                'coffee_menu': None
            },
            {
                'coffee_menu': 'list|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_min_list_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'list|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_missing_key_success(self):
        validator = Validator(
            {
                'missing_key': None,
            },
            {
                'coffee_menu': 'list|nullable|max:3',
            }
        )
    
        self.assert_false(validator.fails())

    def test_min_list_nullable_success(self):
        validator = Validator(
            {
                'coffee_menu': None,
            },
            {
                'coffee_menu': 'list|nullable|min:3',
            }
        )

        self.assert_false(validator.fails())

    def test_max_list_nullable_success(self):
        validator = Validator(
            {
                'coffee_menu': None,
            },
            {
                'coffee_menu': 'list|nullable|max:3',
            }
        )

        self.assert_false(validator.fails())

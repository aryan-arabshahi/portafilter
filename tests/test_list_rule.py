from portafilter.json_schema import JsonSchema
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

    def test_string_list_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso'],
            },
            {
                'coffee_menu': 'required|list:string',
            }
        )

        self.assert_false(validator.fails())

    def test_string_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 2, None],
            },
            {
                'coffee_menu': 'required|list:string',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.list_item_type', attributes={'attribute': 'coffee_menu', 'type': 'string'})]
            }
        )

    def test_integer_list_success(self):
        validator = Validator(
            {
                'coffee_menu': [10],
            },
            {
                'coffee_menu': 'required|list:integer',
            }
        )

        self.assert_false(validator.fails())

    def test_integer_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', 2, None],
            },
            {
                'coffee_menu': 'required|list:integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.list_item_type', attributes={'attribute': 'coffee_menu', 'type': 'integer'})]
            }
        )

    def test_dict_list_success(self):
        validator = Validator(
            {
                'coffee_menu': [{'name': 'espresso'}],
            },
            {
                'coffee_menu': 'required|list:dict',
            }
        )

        self.assert_false(validator.fails())

    def test_dict_list_fail(self):
        validator = Validator(
            {
                'coffee_menu': [{'name': 'espresso'}, 2, None],
            },
            {
                'coffee_menu': 'required|list:dict',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu': [trans('en.list_item_type', attributes={'attribute': 'coffee_menu', 'type': 'dict'})]
            }
        )

    def test_string_list_item_success(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', None, ''],
            },
            {
                'coffee_menu.*': 'string|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_required_string_list_item_fail(self):
        validator = Validator(
            {
                'coffee_menu': ['espresso', None, ''],
            },
            {
                'coffee_menu.*': 'required|string',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu.1': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.1'}),
                    trans('en.string', attributes={'attribute': 'coffee_menu.1'}),
                ],
                'coffee_menu.2': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.2'}),
                ]
            }
        )

    def test_integer_list_item_success(self):
        validator = Validator(
            {
                'coffee_menu': [10, None, 0],
            },
            {
                'coffee_menu.*': 'integer|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_required_integer_list_item_fail(self):
        validator = Validator(
            {
                'coffee_menu': [10, None, 0],
            },
            {
                'coffee_menu.*': 'required|integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu.1': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.1'}),
                    trans('en.integer', attributes={'attribute': 'coffee_menu.1'}),
                ],
            }
        )

    def test_dict_list_item_success(self):
        validator = Validator(
            {
                'coffee_menu': [
                    {
                        'id': 1,
                        'name': 'espresso',
                    },
                    None,
                ],
            },
            {
                'coffee_menu.*': 'dict|nullable',
            }
        )

        self.assert_false(validator.fails())

    def test_required_dict_list_item_fail(self):
        validator = Validator(
            {
                'coffee_menu': [
                    {
                        'id': 1,
                        'name': 'espresso',
                    },
                    None,
                    {},
                ],
            },
            {
                'coffee_menu.*': 'required|dict',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu.1': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.1'}),
                    trans('en.dict', attributes={'attribute': 'coffee_menu.1'}),
                ],
                'coffee_menu.2': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.2'}),
                ],
            }
        )

    def test_dict_item_of_list_item_fail(self):
        validator = Validator(
            {
                'coffee_menu': [
                    {
                        'id': 1,
                        'name': 'espresso',
                    },
                    {
                        'id': 'Test',
                        'name': 'espresso',
                    },
                    {
                        'name': 'espresso',
                    },
                ],
            },
            {
                'coffee_menu.*.id': 'required|integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu.1.id': [
                    trans('en.integer', attributes={'attribute': 'coffee_menu.1.id'}),
                ],
                'coffee_menu.2.id': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.2.id'}),
                    trans('en.integer', attributes={'attribute': 'coffee_menu.2.id'}),
                ],
            }
        )

    def test_nested_dict_item_of_list_item_success(self):
        validator = Validator(
            {
                'coffee_menu': [
                    {
                        'id': 1,
                        'name': 'espresso',
                    },
                    {
                        'id': 2,
                        'name': 'espresso',
                        'ingredients': [
                            {
                                'id': 1,
                                'name': 'Robusta',
                            }
                        ],
                    },
                ],
            },
            {
                'coffee_menu.*.id': 'required|integer',
                'coffee_menu.*.ingredients.*.id': 'integer',
                'coffee_menu.*.ingredients.*.name': 'string',
            }
        )

        self.assert_false(validator.fails())

    def test_nested_dict_item_of_list_item_fail(self):
        validator = Validator(
            {
                'coffee_menu': [
                    {
                        'id': 1,
                        'name': 'espresso',
                    },
                    {
                        'id': 2,
                        'name': 'espresso',
                        'ingredients': [
                            {
                                'id': None,
                                'name': 'Robusta',
                            }
                        ],
                    },
                ],
            },
            {
                'coffee_menu.*.ingredients.*.id': 'required|integer',
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'coffee_menu.0.ingredients.*.id':
                [
                    trans('en.required', attributes={'attribute': 'coffee_menu.0.ingredients.*.id'}),
                    trans('en.integer', attributes={'attribute': 'coffee_menu.0.ingredients.*.id'}),
                ],
                'coffee_menu.1.ingredients.0.id':
                [
                    trans('en.required', attributes={'attribute': 'coffee_menu.1.ingredients.0.id'}),
                    trans('en.integer', attributes={'attribute': 'coffee_menu.1.ingredients.0.id'}),
                ]
            }
        )

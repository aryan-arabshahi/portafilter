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
                'coffee_menu.*': 'string',
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
                'coffee_menu.*': 'integer',
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
                'coffee_menu.2': [
                    trans('en.required', attributes={'attribute': 'coffee_menu.2'}),
                ]
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
                'coffee_menu.*': 'dict',
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





    # def test_dict_item_of_list_item_fail(self):
    #     validator = Validator(
    #         {
    #             'coffee_menu': [
    #                 {
    #                     'id': 1,
    #                     'name': 'espresso',
    #                 },
    #                 {
    #                     'id': 'Test',
    #                     'name': 'espresso',
    #                 },
    #                 {
    #                     'name': 'espresso',
    #                 },
    #             ],
    #         },
    #         {
    #             'coffee_menu.*.id': 'required|integer',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'coffee_menu.1.id': [
    #                 trans('en.integer', attributes={'attribute': 'coffee_menu.1.id'}),
    #             ],
    #             'coffee_menu.2.id': [
    #                 trans('en.required', attributes={'attribute': 'coffee_menu.2.id'}),
    #                 trans('en.integer', attributes={'attribute': 'coffee_menu.2.id'}),
    #             ],
    #         }
    #     )

    # def test_fix(self):
    #     data = {
    #         "coffee_menu.1.id":
    #         [
    #             "The coffee_menu.1.id must be an integer."
    #         ],
    #         "coffee_menu.2.id":
    #         [
    #             "The coffee_menu.2.id field is required.",
    #             "The coffee_menu.2.id must be an integer."
    #         ]
    #     }

    #     result = JsonSchema(data).get_value_details('coffee_menu.1.id.0')
    #     result

from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class TestDateRule(BaseTest):

    def test_required_success(self):
        validator = Validator(
            {
                'date': '2022-12-23',
            },
            {
                'date': 'required|date',
            }
        )

        self.assert_false(validator.fails())

    # def test_required_missing_key_fail(self):
    #     validator = Validator(
    #         {
    #             'missing_key': None,
    #         },
    #         {
    #             'age': 'required|integer',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': [trans('en.required', attributes={'attribute': 'age'})]
    #         }
    #     )

    # def test_required_fail_none_value(self):
    #     validator = Validator(
    #         {
    #             'age': None,
    #         },
    #         {
    #             'age': 'required|integer',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': [
    #                 trans('en.required', attributes={'attribute': 'age'}),
    #                 trans('en.integer', attributes={'attribute': 'age'}),
    #             ]
    #         }
    #     )

    # def test_required_with_zero_value_success(self):
    #     validator = Validator(
    #         {
    #             'age': 0,
    #         },
    #         {
    #             'age': 'required',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_non_integer_value_fail(self):
    #     validator = Validator(
    #         {
    #             'age': '10',
    #         },
    #         {
    #             'age': 'integer',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': [trans('en.integer', attributes={'attribute': 'age'})]
    #         }
    #     )

    # def test_integer_value_success(self):
    #     validator = Validator(
    #         {
    #             'age': 10,
    #         },
    #         {
    #             'age': 'integer',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_required_integer_fail_empty_string(self):
    #     validator = Validator(
    #         {
    #             'age': '',
    #         },
    #         {
    #             'age': 'required|integer',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': [
    #                 trans('en.required', attributes={'attribute': 'age'}),
    #                 trans('en.integer', attributes={'attribute': 'age'}),
    #             ]
    #         }
    #     )

    # def test_min_integer_fail(self):
    #     validator = Validator(
    #         {
    #             'age': 4,
    #         },
    #         {
    #             'age': 'integer|min:5',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': [trans('en.min.numeric', attributes={'attribute': 'age', 'min': 5})]
    #         }
    #     )

    # def test_min_integer_success(self):
    #     validator = Validator(
    #         {
    #             'age': 5,
    #         },
    #         {
    #             'age': 'integer|min:5',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_max_integer_fail(self):
    #     validator = Validator(
    #         {
    #             'age': 4,
    #         },
    #         {
    #             'age': 'integer|max:3',
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': [trans('en.max.numeric', attributes={'attribute': 'age', 'max': 3})]
    #         }
    #     )

    # def test_max_integer_success(self):
    #     validator = Validator(
    #         {
    #             'age': 4,
    #         },
    #         {
    #             'age': 'integer|max:4',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_nullable_missing_key_success(self):
    #     validator = Validator(
    #         {
    #             'missing_key': None,
    #         },
    #         {
    #             'age': 'integer|nullable',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_nullable_success(self):
    #     validator = Validator(
    #         {
    #             'age': None
    #         },
    #         {
    #             'age': 'integer|nullable',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_min_integer_missing_key_success(self):
    #     validator = Validator(
    #         {
    #             'missing_key': None,
    #         },
    #         {
    #             'age': 'integer|min:3',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_max_integer_missing_key_success(self):
    #     validator = Validator(
    #         {
    #             'missing_key': None,
    #         },
    #         {
    #             'age': 'integer|nullable|max:3',
    #         }
    #     )
    
    #     self.assert_false(validator.fails())

    # def test_min_integer_nullable_success(self):
    #     validator = Validator(
    #         {
    #             'age': None,
    #         },
    #         {
    #             'age': 'integer|nullable|min:3',
    #         }
    #     )

    #     self.assert_false(validator.fails())

    # def test_max_integer_nullable_success(self):
    #     validator = Validator(
    #         {
    #             'age': None,
    #         },
    #         {
    #             'age': 'integer|nullable|max:3',
    #         }
    #     )

    #     self.assert_false(validator.fails())

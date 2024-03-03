from typing import Optional
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Model, Ruleset
from portafilter.exceptions import ValidationError


class TestModelIntegerRule(BaseTest):

    def test_required_success(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        User(**{
            'age': 10,
            'count': 20,
        })

    def test_required_missing_key_fail(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        try:
            User()

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'age': [trans('en.present', attributes={'attribute': 'age'})],
                    'count': [
                        trans('en.required', attributes={'attribute': 'count'}),
                        trans('en.integer', attributes={'attribute': 'count'}),
                    ],
                }
            )

    def test_required_fail_none_value(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        try:
            User(**{
                'age': None,
                'count': None,
            })

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'age': [trans('en.integer', attributes={'attribute': 'age'})],
                    'count': [
                        trans('en.required', attributes={'attribute': 'count'}),
                        trans('en.integer', attributes={'attribute': 'count'}),
                    ],
                }
            )

    def test_required_with_zero_value_success(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        User(**{
            'age': 0,
            'count': 0,
        })

    def test_non_integer_value_fail(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        try:
            User(**{
                'age': '10',
                'count': '20',
            })

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'age': [trans('en.integer', attributes={'attribute': 'age'})],
                    'count': [trans('en.integer', attributes={'attribute': 'count'})],
                }
            )

    def test_integer_value_success(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        User(**{
            'age': 10,
            'count': 20,
        })

    def test_required_integer_fail_empty_string(self):
        class User(Model):
            age: int
            count: Ruleset('required|integer')

        try:
            User(**{
                'age': '',
                'count': '',
            })

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'age': [trans('en.integer', attributes={'attribute': 'age'})],
                    'count': [
                        trans('en.required', attributes={'attribute': 'count'}),
                        trans('en.integer', attributes={'attribute': 'count'}),
                    ],
                }
            )

    def test_nullable_success(self):
        class User(Model):
            age: Optional[int]
            count: Ruleset('nullable|integer')

        User(**{
            'age': None,
            'count': None,
        })

    def test_nullable_default_value_success(self):
        class User(Model):
            age: Optional[int] = None
            count: Ruleset('nullable|integer') = None

        User()

    def test_nullable_failed_missing_key(self):
        class User(Model):
            age: Optional[str]
            count: Ruleset('nullable|integer')

        try:
            User()

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'age': [trans('en.present', attributes={'attribute': 'age'})],
                    'count': [trans('en.present', attributes={'attribute': 'count'})],
                }
            )

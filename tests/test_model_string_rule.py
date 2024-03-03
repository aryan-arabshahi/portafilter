from typing import Optional
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Model, Ruleset
from portafilter.exceptions import ValidationError


class TestModelStringRule(BaseTest):

    def test_required_success(self):
        class User(Model):
            username: str
            firstname: Ruleset('required|string')

        User(**{
            'username': 'espresso',
            'firstname': 'mocha',
        })

    def test_required_fail_empty_string(self):
        class User(Model):
            username: str
            firstname: Ruleset('required|string')

        try:
            User(**{
                'username': '',
                'firstname': '',
            })

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'firstname': [trans('en.required', attributes={'attribute': 'firstname'})]
                }
            )

    def test_required_missing_key_fail(self):
        class User(Model):
            username: str
            firstname: Ruleset('required|string')

        try:
            User()

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'firstname': [trans('en.required', attributes={'attribute': 'firstname'})],
                    'username': [trans('en.present', attributes={'attribute': 'username'})],
                }
            )

    def test_required_fail_none_value(self):
        class User(Model):
            username: str
            firstname: Ruleset('required|string')

        try:
            User(**{
                'username': None,
                'firstname': None,
            })

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'firstname': [trans('en.required', attributes={'attribute': 'firstname'})],
                    'username': [trans('en.string', attributes={'attribute': 'username'})],
                }
            )

    def test_non_string_value_fail(self):
        class User(Model):
            username: str
            firstname: Ruleset('string')

        try:
            User(**{
                'username': 10,
                'firstname': 10,
            })

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'firstname': [trans('en.string', attributes={'attribute': 'firstname'})],
                    'username': [trans('en.string', attributes={'attribute': 'username'})],
                }
            )

    def test_string_value_success(self):
        class User(Model):
            username: str
            firstname: Ruleset('string')

        User(**{
            'username': 'espresso',
            'firstname': 'mocha',
        })

    def test_nullable_default_value_success(self):
        class User(Model):
            username: Optional[str] = None
            firstname: Ruleset('nullable|string') = None

        User()

    def test_nullable_failed_missing_key(self):
        class User(Model):
            username: Optional[str]
            firstname: Ruleset('nullable|string')

        try:
            User()

        except ValidationError as e:
            self.assert_json(
                e.errors(),
                {
                    'firstname': [trans('en.present', attributes={'attribute': 'firstname'})],
                    'username': [trans('en.present', attributes={'attribute': 'username'})],
                }
            )

    def test_nullable_success(self):
        class User(Model):
            username: Optional[str]
            firstname: Ruleset('nullable|string')

        User(**{
            'username': None,
            'firstname': None,
        })

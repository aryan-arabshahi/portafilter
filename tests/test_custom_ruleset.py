from typing import Any, List
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator, Rule, Ruleset


class EmailDomainRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[str]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[str]}

        Returns:
            bool
        """
        return value and value.endswith('@codewithcoffee.dev')

    def message(self, attribute: str, value: Any, params: List[str]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[str]}

        Returns:
            str
        """
        return f'The {attribute} is not valid.'


class EmailRuleset(Ruleset):

    rules = 'string|email'


class CustomEmailRuleset(Ruleset):

    rules = [EmailRuleset, EmailDomainRule]


class TestCustomRuleset(BaseTest):

    def test_single_custom_ruleset_success(self):
        validator = Validator(
            {
                'email': 'espresso@codewithcoffee.dev',
            },
            {
                'email': CustomEmailRuleset,
            }
        )

        self.assert_false(validator.fails())

    def test_single_custom_ruleset_fail_invalid_value(self):
        validator = Validator(
            {
                'email': 'espresso',
            },
            {
                'email': CustomEmailRuleset,
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.email', attributes={'attribute': 'email'})
                ],
            }
        )

    def test_single_custom_ruleset_fail_none_value(self):
        validator = Validator(
            {
                'email': None,
            },
            {
                'email': CustomEmailRuleset,
            }
        )

        self.assert_true(validator.fails())

    def test_rules_contains_custom_ruleset_success(self):
        validator = Validator(
            {
                'email': 'espresso@codewithcoffee.dev',
            },
            {
                'email': [CustomEmailRuleset],
            }
        )

        self.assert_false(validator.fails())

    def test_rules_contains_custom_ruleset_fail_invalid_value(self):
        validator = Validator(
            {
                'email': 'espresso',
            },
            {
                'email': [CustomEmailRuleset],
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.email', attributes={'attribute': 'email'})
                ],
            }
        )

    def test_rules_contains_custom_ruleset_fail_required_value(self):
        validator = Validator(
            {
                'email': None,
            },
            {
                'email': ['required', CustomEmailRuleset],
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    trans('en.required', attributes={'attribute': 'email'})
                ],
            }
        )

    def test_rules_contains_custom_ruleset_fail_invalid_email_domain(self):
        validator = Validator(
            {
                'email': 'aryan.arabshahi.programmer@gmail.com',
            },
            {
                'email': ['required', CustomEmailRuleset],
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'email': [
                    'The email is not valid.',
                ],
            }
        )

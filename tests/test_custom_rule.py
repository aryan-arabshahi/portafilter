from typing import Any, List
from tests import BaseTest
from portafilter import Validator, Rule


class AgeVerificationRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[str]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[str]}

        Returns:
            bool
        """
        age_check = self.get_params()[0] if self.get_params() else 18

        return isinstance(value, int) and value >= age_check

    def message(self, attribute: str, value: Any, params: List[str]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[str]}

        Returns:
            str
        """
        return f'The {attribute} must be greater than {params[0]}.'


class TestCustomRule(BaseTest):

    def test_custom_rule_success(self):
        validator = Validator(
            {
                'age': 18,
            },
            {
                'age': ['required', 'integer', AgeVerificationRule(18)],
            }
        )

        self.assert_false(validator.fails())

    def test_custom_rule_fail(self):
        validator = Validator(
            {
                'age': 10,
            },
            {
                'age': ['required', 'integer', AgeVerificationRule(20)],
            }
        )

        self.assert_true(validator.fails())

        self.assert_json(
            validator.errors(),
            {
                'age': ['The age must be greater than 20.']
            }
        )

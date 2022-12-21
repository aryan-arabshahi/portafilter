from typing import Any, List
from portafilter.rules import Rule
from portafilter.utils import trans
from tests import BaseTest
from portafilter import Validator


class MobileVerificationRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return True

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} is not valid.'


class TestCustomRuleset(BaseTest):

    def test_custom_rule_success(self):
        validator = Validator(
            {
                'mobile': '09361909810',
            },
            {
                'mobile': ['required', MobileVerificationRule],
            }
        )

        self.assert_false(validator.fails())

    # def test_custom_rule_fail(self):
    #     validator = Validator(
    #         {
    #             'age': 10,
    #         },
    #         {
    #             'age': ['required', 'integer', AgeVerificationRule(20)],
    #         }
    #     )

    #     self.assert_true(validator.fails())

    #     self.assert_json(
    #         validator.errors(),
    #         {
    #             'age': ['The age must be greater than 20.']
    #         }
    #     )

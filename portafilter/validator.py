from typing import Union, Tuple, Any, List

from portafilter.enums import ValueType
from portafilter.exceptions import ValidationError
from portafilter.rules import RulesList, Ruleset


class Validator:

    def __init__(self, data: dict, rules: dict):
        """The init method

        Arguments:
            data {dict} -- The input data.
            rules {dict} -- The validation rules.
        """
        self._data = data
        self._rules = RulesList(rules)
        self._errors = {}

    def validate(self) -> None:
        """Validate the input data

        Raises:
            ValidationError
        """
        extra_rules = []

        for attribute, ruleset in self._rules:
            try:
                value = self._data.get(attribute)

                ruleset.validate(attribute=attribute, value=value)

                extra_rules += self._get_extra_rules(attribute, value, ruleset)

            except ValidationError as e:
                self._errors[attribute] = ruleset.errors()

        # Validate the extra rules
        for extra_attribute, extra_rule, extra_value in extra_rules:
            try:
                extra_rule.validate(extra_attribute, extra_value)

            except ValidationError as e:
                self._errors[extra_attribute] = extra_rule.errors()

        if self.has_error():
            raise ValidationError

    @staticmethod
    def _get_extra_rules(attribute: str, value: Any, ruleset: Ruleset) -> List[Tuple[str, Ruleset, Any]]:
        """Get the extra rules

        Arguments:
            attribute {str}
            value {Any}
            ruleset {Ruleset}

        Returns:
            List[Tuple[str, Ruleset, Any]]
        """
        extra_rules = []

        if ruleset.get_value_type() == ValueType.DICT:
            for dict_parameter in ruleset.get_rule('dict').get_params():
                extra_attribute = f'{attribute}.{dict_parameter}'

                try:
                    extra_rule_value = value.get(dict_parameter)

                except Exception as e:
                    extra_rule_value = None

                extra_rules.append((extra_attribute, Ruleset('required'), extra_rule_value))

        return extra_rules

    def has_error(self) -> bool:
        """Check the failure status.

        Returns:
            bool
        """
        return True if self._errors else False

    def fails(self) -> bool:
        """Check the status of the validation

        Returns:
            bool
        """
        try:
            self.validate()

        except ValidationError as e:
            pass

        return self.has_error()

    def errors(self) -> dict:
        """Get the errors

        Returns:
            dict
        """
        return self._errors

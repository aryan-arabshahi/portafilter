from copy import deepcopy
from typing import Tuple, Any, List
from portafilter.enums import ValueType
from portafilter.exceptions import ValidationError
from portafilter.json_schema import JsonSchema
from portafilter.rules import RuleList, Ruleset


class Validator:

    def __init__(self, data: dict, rules: dict):
        """The init method

        Arguments:
            data {dict} -- The input data.
            rules {dict} -- The validation rules.
        """
        self._data = data
        self._rules = RuleList(rules)
        self._errors = {}

    def validate(self) -> None:
        """Validate the input data

        Raises:
            ValidationError
        """
        self._clear_errors()

        for attribute, ruleset in self._rules:

            try:
                ruleset = self._modify_dependent_rules(ruleset)

                value_details = JsonSchema(self._data).get_value_details(attribute)

                if isinstance(value_details, list):

                    for list_item in value_details:
                        ruleset_clone = deepcopy(ruleset)
                        item_attribute, item_value_details = self._extract_list_details(attribute, list_item)

                        try:
                            item_value, value_exists = item_value_details

                            ruleset_clone.validate(
                                attribute=item_attribute,
                                value=item_value,
                                value_exists=value_exists
                            )

                        except ValidationError as e:
                            self._errors[item_attribute] = ruleset_clone.errors()

                else:
                    value, value_exists = value_details

                    ruleset.validate(attribute=attribute, value=value, value_exists=value_exists)

            except ValidationError as e:
                self._errors[attribute] = ruleset.errors()

        if self.has_error():
            raise ValidationError(errors=self.errors())

    def _extract_list_details(self, attribute: str, list_details: Tuple[int, Any]) -> Tuple[str, Any]:
        """Extract the list details

        Arguments:
            attribute {str}
            list_details {Tuple[int, Any]}

        Returns:
            Tuple[str, Any] -- The tuple of the attribute and the value.
        """
        _index, _value = list_details
        attribute = attribute.replace('.*', f'.{_index}', 1)
        if isinstance(_value, list) and _value and isinstance(_value[0], tuple):
            # Recursive
            attribute, _value = self._extract_list_details(attribute, _value[0])

        return attribute, _value

    def _clear_errors(self) -> None:
        """Clear the errors.
        """
        self._errors = {}

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

    def passes(self) -> bool:
        """Check the status of the validation

        Returns:
            bool
        """
        try:
            self.validate()

        except ValidationError as e:
            pass

        return not self.has_error()

    def errors(self) -> dict:
        """Get the errors

        Returns:
            dict
        """
        return self._errors

    def _modify_dependent_rules(self, ruleset: Ruleset) -> Ruleset:
        """Modify dependent rules

        Arguments:
            ruleset (Ruleset)

        Returns:
            Ruleset
        """
        # The rules are mutable object
        if ruleset.has_rule('same'):
            same_rule = ruleset.get_rule('same')
            other_attribute = same_rule.get_params()[0]
            other_value_details = JsonSchema(self._data).get_value_details(other_attribute)
            same_rule.add_param(other_value_details)

        if ruleset.has_rule('different'):
            different_rule = ruleset.get_rule('different')
            other_attribute = different_rule.get_params()[0]
            other_value_details = JsonSchema(self._data).get_value_details(other_attribute)
            different_rule.add_param(other_value_details)

        date_related_rule_names = ['after', 'before', 'after_or_equal', 'before_or_equal']

        if ruleset.has_one_of_rules(date_related_rule_names):
            if not ruleset.has_rule('date'):
                ruleset.add_rule('date')

            for rule_name in date_related_rule_names:
                _rule = ruleset.get_rule(rule_name)
                if _rule:
                    _rule_param = _rule.get_params()[0]
                    other_attribute_value_details = JsonSchema(self._data).get_value_details(_rule_param)
                    if isinstance(other_attribute_value_details, tuple) and other_attribute_value_details[1]:
                        _rule.add_param(other_attribute_value_details[0])

        if ruleset.has_rules(['date', 'between']):
            ruleset.set_rule_metadata('between', ('is_date', True))

        return ruleset

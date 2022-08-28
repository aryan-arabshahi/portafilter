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
                value = self._get_value(attribute, self._data)

                if isinstance(value, list):
                    for list_item in value:
                        item_attribute, item_value = self._extract_list_details(attribute, list_item)
                        try:
                            ruleset.validate(attribute=item_attribute, value=item_value)
                            extra_rules += self._get_extra_rules(item_attribute, item_value, ruleset)

                        except ValidationError as e:
                            self._errors[item_attribute] = ruleset.errors()

                else:
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

    def _extract_list_details(self, attribute: str, list_details: Tuple[int, Any]) -> Tuple[str, Any]:
        """Extract the list details

        Arguments:
            attribute {str}
            list_details {Tuple[int, Any]}

        Returns:
            Tuple[str, Any] -- The tuple of the attribute and the value.
        """
        _index, _value = list_details
        attribute = attribute.replace('.*.', f'.{_index}.', 1)
        if isinstance(_value, list) and _value and isinstance(_value[0], tuple):
            # Recursive
            attribute, _value = self._extract_list_details(attribute, _value[0])

        return attribute, _value

    def _get_value(self, attribute: str, data: dict, default_value: Any = None) -> Any:
        """Get the specified attribute value

        Arguments:
            attribute {str}
            data {dict}

        Keyword Arguments:
            default_value {Any}

        Returns:
            Any
        """
        try:
            _key = attribute.split('.')
            iteration = len(_key)

            if iteration > 1:
                result = None
                counter = 1

                for key_holder in _key:

                    if key_holder == '*' and isinstance(result, list):
                        list_result = []
                        list_index = 1
                        for list_item in result:
                            list_item_target_key = '.'.join(_key[counter:])
                            # Recursive
                            list_result.append((list_index, self._get_value(list_item_target_key, list_item)))
                            list_index += 1

                        return list_result

                    if counter == 1:
                        result = data.get(key_holder, {})

                    elif counter < iteration:
                        result = result.get(key_holder, {})

                    else:
                        result = result.get(key_holder, default_value)

                    counter += 1

                return result

            else:
                return data.get(_key[0], default_value)

        except AttributeError as e:
            return default_value

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

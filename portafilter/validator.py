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

            # TODO:@@@@: check the array mode
            if '.*.' in attribute:
                print('Check the array mode')

            try:
                value = self._get_value(attribute)

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

    def _get_value(self, attribute: str, default_value: Any = None) -> Any:
        """Get the specified attribute value

        Arguments:
            attribute {str}

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

                    # # TODO:@@@@: Check the * mode
                    # if key_holder == '*' and isinstance(result, list):
                    #     for list_item in result:
                    #         list_item_target_key = _key[counter]
                    #         result = list_item.get(list_item_target_key, {})
                    #
                    #         result = self._get_value(list_item_target_key)
                    #         print(list_item)
                    #         print(key_holder, result)


                    if counter == 1:
                        result = self._data.get(key_holder, {})

                    elif counter < iteration:
                        result = result.get(key_holder, {})

                    else:
                        result = result.get(key_holder, default_value)

                    counter += 1

                return result

            else:
                return self._data.get(_key[0], default_value)

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

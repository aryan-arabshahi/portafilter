from collections import OrderedDict
from abc import ABC, abstractmethod
from typing import Any, Tuple, List, Union
from portafilter.enums import ValueType
from portafilter.exceptions import InvalidRule, InvalidRuleParam, ValidationError


class Rule(ABC):

    def __init__(self, params: List[Any]):
        """The init method.

        Arguments:
            params {List[Any]}
        """
        self._params = params
        self._value_type = ValueType.STRING

    def get_params(self) -> List[Any]:
        """Get the rule params

        Returns:
            List[Any]
        """
        return self._params

    def set_value_type(self, value_type: ValueType) -> None:
        """Set the value type.
        """
        self._value_type = value_type

    def get_value_type(self) -> ValueType:
        """Get the value type.
        Returns:
            ValueType
        """
        return self._value_type

    @abstractmethod
    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        pass

    @abstractmethod
    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        pass


class RequiredRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return True if value else False

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} field is required.'


class StringRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return isinstance(value, str)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} must be a string.'


class MinRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool

        Raises:
            NotImplementedError
            InvalidRuleParam
        """
        value_type = self.get_value_type()

        try:
            min_value = int(params[0])

        except InvalidRuleParam as e:
            raise e

        if value_type == ValueType.STRING:
            return isinstance(value, str) and len(value) >= min_value

        elif value_type == ValueType.ARRAY:
            return isinstance(value, list) and len(value) >= min_value

        elif value_type == ValueType.INTEGER:
            return isinstance(value, int) and value >= min_value

        elif value_type == ValueType.NUMERIC:
            print('Done...')

        else:
            raise NotImplementedError

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} must be at least {params[0]} characters.'


class MaxRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool

        Raises:
            NotImplementedError
            InvalidRuleParam
        """
        value_type = self.get_value_type()

        try:
            max_value = int(params[0])

        except InvalidRuleParam as e:
            raise e

        if value_type == ValueType.STRING:
            return isinstance(value, str) and len(value) <= max_value

        elif value_type == ValueType.ARRAY:
            return isinstance(value, list) and len(value) <= max_value

        elif value_type == ValueType.INTEGER:
            return isinstance(value, int) and value <= max_value

        elif value_type == ValueType.NUMERIC:
            print('Done...')

        else:
            raise NotImplementedError

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} may not be greater than {params[0]} characters.'


class IntegerRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return isinstance(value, int)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} must be an integer.'


class BooleanRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return isinstance(value, bool)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} field must be true or false.'


class ArrayRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return isinstance(value, list)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} must be an array.'


class DictRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return isinstance(value, dict)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return f'The {attribute} must be a dictionary.'


class KeyExistsRule(Rule):

    def validate(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """The validate method.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        pass

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        pass


class Ruleset:

    def __init__(self, rules: str):
        """The init method

        Arguments:
            rules {str}
        """
        self._rules = self._parse(rules)
        self._set_value_type()
        self._errors = []

    def _parse(self, rules: str) -> OrderedDict:
        """Parse the rules

        Arguments:
            rules {str}
        
        Returns:
            OrderedDict
        """
        parsed_rules = OrderedDict()

        for _rule in rules.split('|'):
            _rule_params = _rule.split(':')
            _rule_name = _rule_params.pop(0)
            _rule_params = self._split_rule_params(_rule_params)

            rule_class = globals().get(f"{_rule_name.capitalize()}Rule")

            if rule_class:
                parsed_rules[_rule_name] = rule_class(_rule_params)

            else:
                raise InvalidRule(f"Invalid rule: {_rule_name}")

        return parsed_rules

    def get_rule(self, rule_name: str) -> Union[Rule, None]:
        """Get the specified rule

        Arguments:
            rule_name {str}

        Returns:
            Union[Rule, None]
        """
        return self._rules.get(rule_name)

    @staticmethod
    def _split_rule_params(rule_params: List[Any]) -> List[Any]:
        """Split the rule params

        Arguments:
            rule_params {List[Any]}

        Returns:
            List[Any]
        """
        return [item for sublist in [rule_param.split(',') for rule_param in rule_params] for item in sublist]

    def get_value_type(self) -> str:
        """Get the value type based on the rules

        Returns:
            str
        """
        value_type = ValueType.STRING

        for rule_name in self._rules.keys():
            try:
                value_type = ValueType(rule_name)
                break

            except ValueError as e:
                pass

        return value_type

    def _set_value_type(self) -> None:
        """Set the rules value type.
        """
        value_type = self.get_value_type()
        for rule_name, rule in self._rules.items():
            rule.set_value_type(value_type)

    def validate(self, attribute: str, value: Any) -> None:
        """Validate the ruleset

        Arguments:
            attribute {str}
            value {Any}

        Raises:
            ValidationError
        """
        for rule_name, rule in self._rules.items():

            # TODO: Remove this
            if rule.validate(attribute, value, rule.get_params()) is None:
                raise Exception(f'The validate method returns NULL - rule_name: {rule_name}')

            if not rule.validate(attribute, value, rule.get_params()):

                self._errors.append(rule.message(attribute, value, rule.get_params()))

                # TODO: Remove this
                if not rule.message(attribute, value, rule.get_params()):
                    raise Exception(f'The message is empty - rule_name: {rule_name}')

        if self.has_error():
            raise ValidationError

    def has_error(self) -> bool:
        """Check the failure status.

        Returns:
            bool
        """
        return True if self._errors else False

    def errors(self) -> list:
        """Get the error messages list.

        Returns:
            list
        """
        return self._errors


class RulesList:

    def __init__(self, rules: dict):
        """The init method

        Arguments:
            rules {dict}
        """
        self._rules = self._parse(rules)

    @staticmethod
    def _parse(rules: dict) -> OrderedDict:
        """Parse the rules

        Returns:
            OrderedDict
        """
        parsed_rules = OrderedDict()

        for attribute, _rules in rules.items():
            parsed_rules[attribute] = Ruleset(_rules)

        return parsed_rules

    def __iter__(self):
        """The iter magic method
        """
        self._iter_current_index = 0
        self._iter_fields = list(self._rules.keys())
        self._iter_fields_count = len(self._iter_fields)
        return self

    def __next__(self) -> Tuple[str, Ruleset]:
        """The next magic method

        Returns:
            Tuple[str, OrderedDict]

        Raises:
            StopIteration
        """
        if self._iter_current_index < self._iter_fields_count:
            attribute = self._iter_fields[self._iter_current_index]
            self._iter_current_index += 1
            return attribute, self._rules[attribute]

        raise StopIteration


# class AddressRuleset(Ruleset):

#     rules = 'required|min:2|max:10'


# class MobileRule(Rule):

#     def validate(self, attribute, value) -> bool:
#         pass

#     def message(self, attribute, value) -> str:
#         pass

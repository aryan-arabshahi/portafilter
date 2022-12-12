from collections import OrderedDict
from abc import ABC, abstractmethod
from typing import Any, Tuple, List, Union
from portafilter.enums import ValueType
from portafilter.exceptions import InvalidRule, InvalidRuleParam, ValidationError
from portafilter.utils import trans


class Rule(ABC):

    def __init__(self, params: List[Any]):
        """The init method.

        Arguments:
            params {List[Any]}
        """
        self._params = params
        self._metadata = {
            'value_type': ValueType.STRING,
        }

    def get_params(self) -> List[Any]:
        """Get the rule params

        Returns:
            List[Any]
        """
        return self._params

    def set_metadata(self, key: str, value: Any) -> None:
        """Set the metadata.

        Arguments:
            key {str}
            value {Any}
        """
        self._metadata[key] = value

    def unset_metadata(self, key: str) -> None:
        """Set the metadata.

        Arguments:
            key {str}
        """
        if key in self._metadata:
            del self._metadata[key]

    def get_metadata(self, key: str) -> Any:
        """Get the metadata.

        Arguments:
            key {str}

        Returns:
            Any
        """
        return self._metadata.get(key)

    def get_value_type(self) -> ValueType:
        """Get the value type.

        Returns:
            ValueType
        """
        return self.get_metadata('value_type')

    def is_required(self) -> bool:
        """The is required check

        Returns:
            bool
        """
        return self.get_metadata('required')

    def is_nullable(self) -> bool:
        """The is nullable check

        Returns:
            bool
        """
        return self.get_metadata('nullable')

    def is_skippable(self, value: Any) -> bool:
        """Skip the rule check

        Arguments:
            value {Any}

        Returns:
            bool
        """
        return value is None and (self.is_nullable() or not self.is_required())

    @abstractmethod
    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

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

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return (self.is_nullable() and value is None) or (True if value else False)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return trans('en.required', attributes={'attribute': attribute})


class NullableRule(Rule):

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
        return ''


class StringRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return self.is_skippable(value) or isinstance(value, str)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return trans('en.string', attributes={'attribute': attribute})


class MinRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

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
        if self.is_skippable(value):
            return True

        value_type = self.get_value_type()

        try:
            min_value = int(params[0])

        except InvalidRuleParam as e:
            raise e

        if value_type == ValueType.STRING:
            return isinstance(value, str) and len(value) >= min_value

        elif value_type == ValueType.LIST:
            return isinstance(value, list) and len(value) >= min_value

        elif value_type == ValueType.INTEGER:
            return isinstance(value, int) and value >= min_value

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
        value_type = self.get_value_type()

        if value_type == ValueType.STRING:
            message_key = 'en.min.string'

        elif value_type == ValueType.LIST:
            message_key = 'en.min.list'

        elif value_type == ValueType.INTEGER:
            message_key = 'en.min.numeric'

        else:
            raise NotImplementedError

        return trans(message_key, attributes={'attribute': attribute, 'min': params[0]})


class MaxRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

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
        if self.is_skippable(value):
            return True

        value_type = self.get_value_type()

        try:
            max_value = int(params[0])

        except InvalidRuleParam as e:
            raise e

        if value_type == ValueType.STRING:
            return isinstance(value, str) and len(value) <= max_value

        elif value_type == ValueType.LIST:
            return isinstance(value, list) and len(value) <= max_value

        elif value_type == ValueType.INTEGER:
            return isinstance(value, int) and value <= max_value

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
        value_type = self.get_value_type()

        if value_type == ValueType.STRING:
            message_key = 'en.max.string'

        elif value_type == ValueType.LIST:
            message_key = 'en.max.list'

        elif value_type == ValueType.INTEGER:
            message_key = 'en.max.numeric'

        else:
            raise NotImplementedError

        return trans(message_key, attributes={'attribute': attribute, 'max': params[0]})


class IntegerRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return self.is_skippable(value) or isinstance(value, int)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            strp
        """
        return trans('en.integer', attributes={'attribute': attribute})


class BooleanRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return self.is_skippable(value) or isinstance(value, bool)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return trans('en.boolean', attributes={'attribute': attribute})


class ListRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        result = self.is_skippable(value) or isinstance(value, list)

        if result and params and value:

            list_item_type = ValueType(params[0])

            for list_item in value:

                if list_item_type == ValueType.DICT:

                    if not isinstance(list_item, dict):
                        return False

                elif list_item_type == ValueType.STRING:

                    if not isinstance(list_item, str):
                        return False

                elif list_item_type == ValueType.INTEGER:

                    if not isinstance(list_item, int):
                        return False

                else:
                    raise NotImplementedError

        return result

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        _key = None
        _attributes = {'attribute': attribute}

        if params:
            _key = 'list_item_type'
            _attributes['type'] = params[0]

        else:
            _key = 'list'

        return trans(f'en.{_key}', attributes=_attributes)


class DictRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            bool
        """
        return self.is_skippable(value) or isinstance(value, dict)

    def message(self, attribute: str, value: Any, params: List[Any]) -> str:
        """The validation error message.

        Arguments:
            attribute {str}
            value {Any}
            params {List[Any]}

        Returns:
            str
        """
        return trans('en.dict', attributes={'attribute': attribute})


class KeyExistsRule(Rule):

    def passes(self, attribute: str, value: Any, params: List[Any]) -> bool:
        """Determine if the validation rule passes.

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
        self._set_rules_metadata()
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

    def get_value_type(self) -> ValueType:
        """Get the value type based on the rules

        Returns:
            ValueType
        """
        value_type = ValueType.STRING

        for rule_name in self._rules.keys():
            try:
                value_type = ValueType(rule_name)
                break

            except ValueError as e:
                pass

        return value_type

    def _set_rules_metadata(self) -> None:
        """Set the rules metadata.
        """
        value_type = self.get_value_type()
        is_required = 'required' in self._rules
        is_nullable = 'nullable' in self._rules
        for rule_name, rule in self._rules.items():
            rule.set_metadata('value_type', value_type)
            rule.set_metadata('required', is_required)
            rule.set_metadata('nullable', is_nullable)

    def validate(self, attribute: str, value: Any, existed_value: bool = True) -> None:
        """Validate the ruleset

        Arguments:
            attribute {str}
            value {Any}

        Keyword Arguments:
            existed_value {bool} -- The value exists in the main data (default: {True})

        Raises:
            ValidationError
        """
        for rule_name, rule in self._rules.items():

            rule.set_metadata('existed_value', existed_value)

            # # TODO: Remove this - its for debug only, you must delete it
            # if rule.passes(attribute, value, rule.get_params()) is None:
            #     raise Exception(f'The validate method returns NULL - rule_name: {rule_name}')

            if not rule.passes(attribute, value, rule.get_params()):

                self._errors.append(rule.message(attribute, value, rule.get_params()))

                # # TODO: Remove this
                # if not rule.message(attribute, value, rule.get_params()):
                #     raise Exception(f'The message is empty - rule_name: {rule_name}')

            rule.unset_metadata('existed_value')

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

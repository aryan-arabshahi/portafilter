from typing import Tuple, Optional, Union, Dict, List, Set, Any
from portafilter.validator import Validator
from portafilter.rules import Ruleset, RulesList
from portafilter.exceptions import ValidationError


class TypeParser:

    PORTAFILTER_TYPE_MAP = {
        type(None): 'nullable',
        str: 'string',
        int: 'integer',
        list: 'list',
        dict: 'dict',
    }

    def get_rules_list(self, attr_name: Any, annotated_type: Any) -> RulesList:
        if isinstance(annotated_type, type):
            return RulesList(
                {
                    attr_name: self._get_rule_by_type(annotated_type),
                }
            )

        elif annotated_type.__module__ == 'typing':
            return RulesList(self._get_rules_by_typing(attr_name, annotated_type))

        else:
            raise NotImplementedError

    def _get_attribute_type(self, annotated_type: Any) -> str:
        ruleset_type = self.PORTAFILTER_TYPE_MAP.get(annotated_type)

        if not ruleset_type:
            raise NotImplementedError

        return ruleset_type

    def _get_rule_by_type(self, annotated_type: Any) -> Ruleset:
        return Ruleset(self._get_attribute_type(annotated_type))

    def _get_rules_by_typing(self, attr_name: Any, annotated_type: Any) -> Dict[str, Ruleset]:
        rules = {}
        args = getattr(annotated_type, '__args__', [])
        origin = getattr(annotated_type, '__origin__', None)

        if isinstance(origin, type):

            if origin in [list, dict]:
                rules[attr_name] = Ruleset(f'{self._get_attribute_type(origin)}')
                if args:
                    item_attr_name = f'{attr_name}.*'
                    rules.update(TypeParser().get_rules_list(item_attr_name, args[0]).get_rules())
            else:
                raise NotImplementedError

        elif origin is Union:
            rules_list = [self._get_attribute_type(union_type) for union_type in args]
            rules[attr_name] = Ruleset('|'.join(rules_list))

        else:
            raise NotImplementedError

        return rules


class ModelMetaclass(type):

    def __call__(cls, *args, **kwargs):

        instance = super().__call__(*args, **kwargs)

        data, validation_rules, nested_attributes = cls.__get_metadata(instance, kwargs)

        validation_errors = cls.__get_validation_errors(data, validation_rules, nested_attributes)
        if validation_errors:
            raise ValidationError(errors=validation_errors)

        # Setting the class attribute
        for attribute, value in data.items():
            setattr(instance, attribute, value)

        return instance

    @staticmethod
    def __get_validation_errors(data: dict, validation_rules: dict, nested_attributes: list) -> dict:
        validation_errors = {}

        # Validating the data
        validator = Validator(data, validation_rules)

        if validator.fails():
            validation_errors = validator.errors()

        # Validating the nested models
        for nested_attribute, nested_model in nested_attributes:
            try:
                data[nested_attribute] = nested_model(**data[nested_attribute])

            except ValidationError as e:
                for error_key, error_messages in e.errors().items():
                    nested_key = f'{nested_attribute}.{error_key}'
                    validation_errors[nested_key] = error_messages

        return validation_errors

    def __get_metadata(cls, instance, kwargs: dict) -> Tuple[dict, dict, list]:
        data = {}
        validation_rules = {}
        nested_attributes = []
        type_parser = TypeParser()

        for attr_name, attr_annotation in cls.__annotations__.items():

            if isinstance(attr_annotation, Ruleset):
                if not attr_annotation.has_rule('present'):
                    attr_annotation.add_rule('present')
                validation_rules[attr_name] = attr_annotation

            elif isinstance(attr_annotation, ModelMetaclass):
                validation_rules[attr_name] = Ruleset('present')
                nested_attributes.append((attr_name, attr_annotation))

            elif isinstance(attr_annotation, type) or attr_annotation.__module__ == 'typing':
                rules_list = type_parser.get_rules_list(attr_name, attr_annotation)

                # Force present the attribute
                for _rule in rules_list:
                    _rule[1].add_rule('present')

                validation_rules.update(rules_list.get_rules())

            if attr_name in kwargs:
                data[attr_name]     = kwargs[attr_name]

            elif hasattr(instance, attr_name):
                data[attr_name] = getattr(instance, attr_name)

        return data, validation_rules, nested_attributes


class Model(metaclass=ModelMetaclass):

    def __init__(self, *args, **kwargs):
        attributes = self._get_attributes()
        for attribute_name, attribute_value in kwargs.items():
            if attribute_name not in attributes:
                raise AttributeError(f"{self.__class__.__name__} object has no attribute '{attribute_name}'")
            setattr(self, attribute_name, attribute_value)

    def _get_attributes(self) -> List[str]:
        """Get the class attributes.

        Returns:
            List[str]
        """
        attributes = []
        for attribute in self.__class__.__dict__:
            if not attribute.startswith("__"):
                attributes.append(attribute)
        return list(set(attributes + list(self.__annotations__.keys())))

    def dict(self) -> dict:
        result = {}

        for attribute in self._get_attributes():
            attribute_value = getattr(self, attribute)
            result[attribute] = attribute_value.dict() if isinstance(attribute_value, Model) else attribute_value

        return result

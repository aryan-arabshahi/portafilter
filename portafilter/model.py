from typing import List, Any
from portafilter.validator import Validator
from portafilter.rules import Ruleset


class ModelMetaclass(type):

    def __call__(cls, *args, **kwargs):
        validation_rules = {}
        data = {}

        instance = super().__call__(*args, **kwargs)

        for attr_name, attr_annotation in cls.__annotations__.items():
            # TODO:@@@@: Check this logic when setting the instance values
            # TODO:@@@@: If there was no value assigmenet and no default value and no validation error for that field
            # TODO:@@@@: Just raise this error
            # TODO:@@@@: OR
            # TODO:@@@@: 
            # TODO:@@@@: Just simply add a required rule in the cases that the field
            # TODO:@@@@: doesn't fill and no validation error with no default value!
            # TODO:@@@@: after the data[attr_name] = getattr(instance, attr_name)
            # if not hasattr(instance, attr_name) and attr_name not in kwargs:
            #     raise TypeError(f"{cls.__name__}.__init__() missing required positional argument: '{attr_name}'")

            if isinstance(attr_annotation, Ruleset):
                validation_rules[attr_name] = attr_annotation

            if attr_name in kwargs:
                data[attr_name] = kwargs[attr_name]

            elif hasattr(instance, attr_name):
                data[attr_name] = getattr(instance, attr_name)

        # Validating the data.
        Validator(data, validation_rules).validate()

        # Setting the class attribute
        for attribute, value in data.items():
            setattr(instance, attribute, value)

        return instance


class Model(metaclass=ModelMetaclass):

    def __init__(self, *args, **kwargs):
        attributes = self.__get_attributes()
        for attribute_name, attribute_value in kwargs.items():
            if attribute_name not in attributes:
                raise AttributeError(f"{self.__class__.__name__} object has no attribute '{attribute_name}'")
            setattr(self, attribute_name, attribute_value)

    def __get_attributes(self) -> List:
        """Get the class attributes.

        Returns:
            List
        """
        attributes = []
        for attribute in self.__class__.__dict__:
            if not attribute.startswith("__"):
                attributes.append(attribute)

        return list(set(attributes + list(self.__annotations__.keys())))

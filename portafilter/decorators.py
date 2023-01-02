from functools import wraps
from .validator import Validator


def validate(**rules):

    def args_validator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = {}
            variable_names = f.__code__.co_varnames[:f.__code__.co_argcount]

            _index = 0
            for _arg in args:
                data[variable_names[_index]] = _arg
                _index += 1

            validator = Validator(
                data={**data, **kwargs},
                rules=rules
            )

            # It raises the ValidationError
            validator.validate()

            return f(*args, **kwargs)

        return wrapper

    return args_validator

from typing import Optional


class InvalidRule(Exception):
    pass


class InvalidRuleParam(Exception):
    pass


class ValidationError(Exception):

    def __init__(self, errors: Optional[dict] = None):
        super().__init__()
        self._errors = errors or {}

    def get_errors(self) -> dict:
        """Get the validation errors

        Returns:
            dict
        """
        return self._errors

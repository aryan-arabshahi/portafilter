from typing import Optional

from portafilter.exceptions import ValidationError
from tests import BaseTest
from portafilter import validate


@validate(name='required|string', microfoam='required|boolean', chocolate='required|numeric', sugar='boolean')
def make_coffee(name: str, microfoam: bool, chocolate: float, sugar: Optional[bool] = False) -> None:
    """The make coffee method.

    Arguments:
        name (str) -- The coffee name.
        microfoam (bool) -- The microfoam.
        chocolate (float) -- The chocolate in grams.

    Keyword Arguments:
        sugar (Optional[bool]) -- The sugar flag (default False)
    """
    pass


class EspressoMachine:

    @validate(name='required|string', microfoam='required|boolean', chocolate='required|numeric', sugar='boolean')
    def make_coffee(self, name: str, microfoam: bool, chocolate: float, sugar: Optional[bool] = False) -> None:
        """The make coffee method.

        Arguments:
            name (str) -- The coffee name.
            microfoam (bool) -- The microfoam.
            chocolate (float) -- The chocolate in grams.

        Keyword Arguments:
            sugar (Optional[bool]) -- The sugar flag (default False)
        """
        pass


class TestDecoratorRule(BaseTest):

    def test_decorator_on_method_success(self):
        make_coffee('Espresso', True, chocolate=10)

    def test_decorator_on_method_fail(self):
        try:
            make_coffee('Espresso', True, chocolate=10, sugar=None)
            assert False

        except ValidationError as e:
            pass

    def test_decorator_on_class_method_success(self):
        EspressoMachine().make_coffee('Espresso', True, chocolate=10)

    def test_decorator_on_class_method_fail(self):
        try:
            EspressoMachine().make_coffee('Espresso', True, chocolate=10, sugar=None)
            assert False

        except ValidationError as e:
            pass

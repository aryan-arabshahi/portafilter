from portafilter import Model, Ruleset
from typing import Optional

from portafilter.exceptions import ValidationError


class Rule:
    def __init__(self, rules: str):
        pass


class User(Model):
    firstname: Ruleset('required|string') = None
    lastname: Ruleset('string|min:5|max:10')
    # lastname: str
    email: Ruleset('required|email') = 'asdasd'


def main():

    try:
        user = User(**{'email': 'angel@gmail.com', 'firstname': 'Test'})
        print(user.email)
        print(user.lastname)

    except ValidationError as e:
        print(e.errors())
        # raise e


if __name__ == '__main__':
    main()

from portafilter import Model, Ruleset
from typing import Optional
from portafilter.exceptions import ValidationError


class User(Model):
    firstname: Ruleset('string')
    email: Ruleset('string|nullable') = None


def main():

    try:
        user = User(firstname="test")
        # print(user.email)
        user.dict()
        # user = User(email='angel@gmail.com', test=123123)
        # print(user.email)
        # print(user.lastname)
        # print(user.email)

    except ValidationError as e:
        print(e.errors())
        # raise e


if __name__ == '__main__':
    main()

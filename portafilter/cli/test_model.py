from portafilter import Model, Ruleset
from portafilter.exceptions import ValidationError


class Address(Model):
    country: str
    city: str
    street: str
    zip_code: str


class Company(Model):
    name: str
    website: str
    address: Address


class User(Model):
    firstname: Ruleset('string')
    lastname: Ruleset('string')
    email: Ruleset('string|nullable') = None
    settings: Ruleset('list:dict')
    company: Company


def main():

    try:
        user = User(
            firstname='Aryan',
            lastname='Arabshahi',
            settings=[
                {
                    'name': 'notifications',
                    'value': True
                }
            ],
            company={
                'name': 'CodeWithCoffee',
                'website': 'codewithcoffee.dev',
                'address': {
                    'country': 'Germany',
                    'city': 'Berlin',
                    'street': 'xxxx',
                    'zip_code': 'xxxx'
                }
            }
        )

        # print(user.email)
        print(user.dict())
        # user = User(email='angel@gmail.com', test=123123)
        # print(user.email)
        # print(user.lastname)
        # print(user.email)

    except ValidationError as e:
        print(e.errors())
        # raise e


if __name__ == '__main__':
    main()

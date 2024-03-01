from typing import Optional, Tuple, Union, Set, Dict, List
from portafilter import Model, Ruleset, Validator
from portafilter.exceptions import ValidationError


# config = {
#     'default_connection': 'foo',
#     'connections': {
#         'foo': {
#             'driver': 'mysql',
#             'host': '127.0.0.1',
#             'port': 3306,
#             'username': 'root',
#             'password': 'toor',
#         },
#         'bar': {
#             'driver': 'mysql',
#             'host': '127.0.0.1',
#             'port': 3306,
#             'username': 'root',
#             'password': 'toor',
#         },
#     },
# }


# class Connection(Model):
#     driver: str
#     host: str
#     port: int
#     database: str
#     username: str
#     password: str


# class Config(Model):
#     default_connection: str
#     connections: List[Connection]


# config = Config(**{
#     'default': 'mysql',
#     'connections': {
#         'mysql': Connection(**{
#             'driver': 'mysql',
#             'host': '127.0.0.1',
#             'port': 3306,
#             'database': 'codewithcoffee.dev',
#             'username': 'root',
#             'password': 'toor',
#         }),
#         'foo': Connection(**{
#             'driver': 'mysql',
#             'host': '127.0.0.1',
#             'port': 3306,
#             'username': 'root',
#             'password': 'toor',
#         }),
#     }
# })


# database_manager = DatabaseManager(config=config)


class Address(Model):
    country: str
    city: str
    street: str
    zip_code: str


class Company(Model):
    name: str
    website: str
    address: Address


# class User(Model):
#     firstname: Ruleset('string')
#     lastname: Ruleset('string')
#     email: Ruleset('string|nullable') = None
#     settings: Ruleset('list:dict')
#     company: Company


class User(Model):
    # username: Optional[str]
    username: Tuple[str, int]
    # username: List[Union[str, int]]
    # username: List[List[str]]
    # username: Dict[str, List[str]]
    # tuple_field: Tuple[str, str, int]
    # firstname: Optional[str]
    # lastname: List[str]
    # tuple_key: Tuple[str, int]
    # union_key: Union[str, int]
    # set_key: Set[int]
    # set_key: Dict[str, int]
    # age: int


def main():

    try:

        # data = {
        #     'names': ['1', '2', 3, '4'],
        # }
        # validator = Validator(
        #     data,
        #     {
        #         'names': 'list',
        #         'names.*': 'string',
        #     }
        # )
        # validator.validate()


        # user = User(
        #     firstname='Aryan',
        #     lastname='Arabshahi',
        #     settings=[
        #         {
        #             'name': 'notifications',
        #             'value': True
        #         }
        #     ],
        #     company={
        #         'name': 'CodeWithCoffee',
        #         'website': 'codewithcoffee.dev',
        #         'address': {
        #             'country': 'Germany',
        #             'city': 'Berlin',
        #             'street': 'xxxx',
        #             'zip_code': 'xxxx'
        #         }
        #     }
        # )

        user = User(
            # username=['1', '2', '3', '4', 5]
            username=[
                {
                    'id': 1,
                    'name': 'Aryan',
                },
                True
            ]
            # username={'name': 'Aryan'}
            # username=[['1', '2'], ['3', 4], ['5']]
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

from portafilter import Validator


def main():
    validator = Validator(
        {
            'name': 'Aryan',
            'amount': 10,
            'products': [
                {
                    'id': 1,
                    'name': 'Aryan',
                    'nickname': 'Angel',
                    'verified': False,
                }
            ],
            'user': {
                'id': 'aksjfhakjshdjashd',
                'username': 'aryan',
                'password': '123456',
                'settings': {
                    'is_valid_user': 123123,
                    'email': True,
                },
            },
        },
        {
            # 'name': 'required|string|min:3|max:4',
            # 'amount': 'required|integer|min:5|max:10',
            # 'products': 'required|array|min:5|max:10',
            # 'user': 'required|dict:username,test',
            # 'user.id': 'required|integer',
            # 'user.settings.is_valid_user': 'required|integer',
            # 'user.settings.email': 'required|boolean',
            'products.*.verified': 'required|boolean',
        }
    )

    # validator.validate()

    if validator.fails():
        print(validator.errors())


if __name__ == '__main__':
    main()

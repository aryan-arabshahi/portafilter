from portafilter import Validator


def main():
    validator = Validator(
        {
            'score': None,
            'name': 'Aryan',
            'amount': 10,
            'products': [
                {
                    'id': 1,
                    'name': 'Aryan',
                    'nickname': 'Angel',
                    'verified': False,
                    'prices': [
                        {
                            'id': 1,
                        },
                    ]
                },
                {
                    'id': 1,
                    'name': 'Aryan',
                    'nickname': 'Angel',
                    'prices': [123123],
                },
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
            'emails': [123123],
        },
        {
            # 'name': 'required|string|min:3|max:4',
            # 'amount': 'required|integer|min:5|max:10',
            # 'products': 'required|list|min:5|max:10',
            # 'user': 'required|dict:username,test',
            # 'user.id': 'required|integer',
            # 'user.settings.is_valid_user': 'required|integer',
            # 'user.settings.email': 'required|boolean',
            # 'name': 'required|string',
            # 'products.*.verified': 'required|boolean',
            # 'products.*.prices.*.id': 'integer',
            # 'products.*.prices': 'list:dict',
            'products.*.prices.*.id': 'integer',
            'products.*.prices.*.name': 'required|string',
            # 'score': 'required|integer',
            # 'emails': 'list:integer',
        }
    )

    # validator.validate()

    if validator.fails():
        print(validator.errors())


if __name__ == '__main__':
    main()

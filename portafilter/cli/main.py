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
                }
            ],
            'user': {
                'username': 'aryan',
                'password': '123456',
            },
        },
        {
            'name': 'required|string|min:3|max:4',
            'amount': 'required|integer|min:5|max:10',
            'products': 'required|array|min:5|max:10',
            'user': 'required|dict:username,test',
        }
    )

    # validator.validate()

    if validator.fails():
        print(validator.errors())


if __name__ == '__main__':
    main()

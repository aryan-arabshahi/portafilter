# Portafilter

Powerful and simple data validation functionality.

---

**Portafilter** provides several different approaches to validate your application's incoming data.  It's **zero dependencies** and easy to use.

## Help

See **[documentation](https://portafilter.dev)** for more details.

## Installation

It's on [PyPI](https://pypi.org/project/portafilter) and all you need to do is:
```
pip install portafilter
```

## A Simple Example

```py
from portafilter import Validator

validator = Validator(
    {
        'name': 'Flat White',
        'description': 'A Flat White is a coffee drink consisting of espresso with microfoam ',
        'ingredients': [
            {
                'name': 'Espresso',
            },
            {
                'name': 'Steamed Milk',
            }
        ],
    },
    {
        'name': 'required',
        'description': 'required|max:255',
        'ingredients': 'required|list',
        'ingredients.*.name': 'required|string',
    }
)

if validator.fails():
    # The data is not valid
    print(validator.errors())

# The data is valid
```

To see all the features, visit [portafilter.dev](https://portafilter.dev)

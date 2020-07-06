# django-address-app

Welcome to Django Address

[![Python Version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/)
[![codecov](https://codecov.io/gh/onufrienkovi/django-address-app/branch/master/graph/badge.svg)](https://codecov.io/gh/onufrienkovi/django-address-app)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)


## Quickstart

Install

```console
pip install django-address-app
```

Add them to your INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'django_address',
    ...
]
```

If you want to use your models and don't want to subclass Abstract models, you must inform django_address about your models in settings.py:

```python
# myproject/settings.py
DJANGO_ADDRESS_COUNTRY_MODEL = "my_app.Country"
DJANGO_ADDRESS_REGION_MODEL = "my_app.Region" # or my_app.State, my_app.Province, etc..
DJANGO_ADDRESS_DISTRICT_MODEL = "my_app.District" # or my_app.County
DJANGO_ADDRESS_LOCALITY_MODEL = "my_app.Locality"
DJANGO_ADDRESS_STREET_MODEL = "my_app.Street"
DJANGO_ADDRESS_ADDRESS_MODEL = "my_app.Address"
```

If you want change behavior processing AddressField, you can use your Service

```python
# myproject/settings.py
DJANGO_ADDRESS_SERVICE_CLASS = "django_address.service.Address"
```

## Example

```python
from django.db import models
from django_address.fields import AddressField

class Order(models.Model):
    """Order model."""
    delivery_address = AddressField(verbose_name="Delivery address")
```

Setting value:

using dict - required field 'raw' only
```python 
obj.address = {
            "raw": "Volodymyrska st, 10",
            "country": "Ukraine",  # can use pk or instance country model
            "country_code": "UA",
            "region": "Kyiv City",  # can use pk or instance Region model
            "region_code": "UA-32",
            "district": "",  # can use pk or instance District model
            "district_code": "",
            "locality": "Kiev",
            "street": "Volodymyrska street",  # can use pk or instance Street model
            "street_number": "10",
            "postal_code": "02000",
            "latitude": 50.456302,
            "longitude": 30.517044,
            "formatted_address": "Khreschatyk St, 15, Kyiv, Ukraine, 02000",
        }

```
or

```python
obj.address = address # pk or Address model instance
```


## Prerequisites

You will need:

- `python3.8` (see `pyproject.toml` for full version)
- `django` with version `3.0`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`pipenv`](https://github.com/pypa/pipenv) (**required**)
- `pycharm 2017+` or `vscode`


## Alternatives
   - [django-address](https://github.com/furious-luke/django-address)
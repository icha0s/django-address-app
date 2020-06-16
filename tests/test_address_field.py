import json

from django.test import TestCase

from django_address.models import Country, District, Region, Locality, Street, Address
from example.order.models import Order
from django.core.exceptions import ValidationError


class AddressFieldTestCase(TestCase):
    def setUp(self):
        self.address1 = {
            "raw": "Khreschatyk st, 15",
            "country": "Ukraine",
            "country_code": "UA",
            "region": "Kyiv City",
            "locality": "Kiev",
            "street": "Khreschatyk street",
            "street_number": "15",
            "postal_code": "02000",
            "latitude": 50.4474875,
            "longitude": 30.524732,
            "formatted_address": "Khreschatyk St, 15, Kyiv, Ukraine, 02000"
        }
        self.address2 = {
            "raw": "Volodymyrska st, 10",
            "country": "Ukraine",
            "country_code": "UA",
            "region": "Kyiv City",
            "locality": "Kiev",
            "street": "Volodymyrska street",
            "street_number": "10",
            "postal_code": "02000",
            "latitude": 50.456302,
            "longitude": 30.517044,
            "formatted_address": "Khreschatyk St, 15, Kyiv, Ukraine, 02000"
        }
        self.address3 = {
            "raw": "Ushakova st, 50",
            "country": "Ukraine",
            "country_code": "UA",
            "region": "Kherson region",
            "locality": "Kherson",
            "street": "Ushakova Avenue",
            "street_number": "51",
            "postal_code": "73009",
            "latitude": 46.6490074,
            "longitude": 32.6104799,
            "formatted_address": "Ushakova Ave, 50, Kherson, Khersons'ka oblast, Ukraine, 73009"
        }
        self.address4 = {
            "raw": "Ushakova st, 51",
            "country": "Ukraine",
            "country_code": "UA",
            "region": "Kherson region",
            "locality": "Kherson",
            "street": "Ushakova Avenue",
            "street_number": "51",
            "postal_code": "73009",
            "latitude": 46.6490075,
            "longitude": 32.6104798,
            "formatted_address": "Ushakova Ave, 50, Kherson, Khersons'ka oblast, Ukraine, 73009"
        }

        self.order1 = Order.objects.create(price="100", delivery_address=self.address1)
        self.order2 = Order.objects.create(price="150", delivery_address=self.address2)
        self.order3 = Order.objects.create(price="200", delivery_address=self.address3)
        self.order4 = Order.objects.create(price="250", delivery_address=self.address4)

        self.field_address1 = {'country': {'code': '', 'country': 1, 'id': 1, 'name': 'Kyiv City'},
                               'formatted_address': 'Khreschatyk St, 15, Kyiv, Ukraine, 02000',
                               'latitude': 50.4474875,
                               'locality': {'district': None,
                                            'id': 1,
                                            'name': 'Kiev',
                                            'postal_code': '02000',
                                            'region': 1,
                                            'slug': 'kiev'},
                               'longitude': 30.524732,
                               'raw': 'Khreschatyk st, 15',
                               'region': {'code': '', 'country': 1, 'id': 1, 'name': 'Kyiv City'},
                               'route': 'Khreschatyk street',
                               'street': {'id': 1, 'locality': 1, 'name': 'Khreschatyk street'},
                               'street_number': '15'}

        self.field_address4 = {'country': {'code': '', 'country': 1, 'id': 2, 'name': 'Kherson region'},
                               'formatted_address': "Ushakova Ave, 50, Kherson, Khersons'ka oblast, Ukraine, "
                                                    '73009',
                               'latitude': 46.6490075,
                               'locality': {'district': None,
                                            'id': 2,
                                            'name': 'Kherson',
                                            'postal_code': '73009',
                                            'region': 2,
                                            'slug': 'kherson'},
                               'longitude': 32.6104798,
                               'raw': 'Ushakova st, 51',
                               'region': {'code': '', 'country': 1, 'id': 2, 'name': 'Kherson region'},
                               'route': 'Ushakova Avenue',
                               'street': {'id': 3, 'locality': 2, 'name': 'Ushakova Avenue'},
                               'street_number': '51'}

    def test_objects_count(self):
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(Region.objects.count(), 2)
        self.assertEqual(District.objects.count(), 0)
        self.assertEqual(Locality.objects.count(), 2)
        self.assertEqual(Street.objects.count(), 3)
        self.assertEqual(Address.objects.count(), 4)

    def test_address_to_dict(self):
        self.assertEqual(self.field_address1, self.order1.delivery_address.to_dict())
        self.assertEqual(self.field_address4, self.order4.delivery_address.to_dict())

    def test_address_to_json(self):
        self.assertEqual(self.field_address1, json.loads(self.order1.delivery_address.to_json()))
        self.assertEqual(self.field_address4, json.loads(self.order4.delivery_address.to_json()))

    def test_validate_value_str(self):
        with self.assertRaises(ValidationError):
            Order.objects.create(price="250", delivery_address="Ushakova st, 51")

    def test_validate_value_dict(self):
        with self.assertRaises(ValidationError):
            Order.objects.create(price="250", delivery_address={})

    def test_validate_value_none(self):
        order = Order.objects.create(price="250")
        self.assertIsNone(order.delivery_address)

    def test_validate_value_address(self):
        order = Order.objects.create(price="250", delivery_address=self.order1.delivery_address)
        self.assertEqual(order.delivery_address, self.order1.delivery_address)

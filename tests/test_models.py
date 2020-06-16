from django.db import IntegrityError
from django.test import TestCase

from django_address.models import Country, District, Locality, Region, Street


class ModelsTestCase(TestCase):
    def setUp(self):
        self.ua = Country.objects.create(name="Ukraine", code="UA")
        self.fr = Country.objects.create(name="France", code="FR")
        self.au = Country.objects.create(name="Australia", code="AU")

        self.ua_kv = Region.objects.create(name="Kyiv", code="KV", country=self.ua)
        self.ua_ks = Region.objects.create(name="Kherson region", code="KS", country=self.ua)
        self.fr_nor = Region.objects.create(name="Normandie", code="NOR", country=self.fr)
        self.fr_occ = Region.objects.create(name="Occitanie", code="OCC", country=self.fr)
        self.au_qld = Region.objects.create(name="Queensland", code="QLD", country=self.au)

        self.ua_kv_obolon = District.objects.create(name="Obolon", region=self.ua_kv)
        self.fr_nor_bessin = District.objects.create(name="Bessin", region=self.fr_nor)
        self.fr_nor_perche = District.objects.create(name="Perche", region=self.fr_nor)
        self.fr_occ_gard = District.objects.create(name="Gard", code="30", region=self.fr_occ)

        self.kiev = Locality.objects.create(name="Kiev", region=self.ua_kv)
        self.kherson = Locality.objects.create(name="Kherson", region=self.ua_ks)
        self.bayeux = Locality.objects.create(name="Bayeux", region=self.fr_nor, district=self.fr_nor_bessin)
        self.aube = Locality.objects.create(name="Aube", region=self.fr_nor, district=self.fr_nor_perche)
        self.essay = Locality.objects.create(name="Essay", region=self.fr_nor, district=self.fr_nor_perche)

        self.street1 = Street.objects.create(name="Ushakova Avenue", locality=self.kherson)
        self.street2 = Street.objects.create(name="Soborna Street", locality=self.kherson)
        self.street3 = Street.objects.create(name="Teatralna Street", locality=self.kherson)

    def test_countries(self):
        countries = Country.objects.all()
        self.assertEqual(countries.count(), 3)
        self.assertListEqual(list(countries), [self.au, self.fr, self.ua])
        self.assertRaises(IntegrityError, Country.objects.create, name="Ukraine", code="UA")

    def test_regions(self):
        regions = Region.objects.all()
        self.assertEqual(regions.count(), 5)
        self.assertListEqual(list(regions), [self.au_qld, self.fr_nor, self.fr_occ, self.ua_ks, self.ua_kv])
        with self.assertRaises(IntegrityError):
            Region.objects.create(name="Kyiv", country=self.ua)

    def test_districts(self):
        districts = District.objects.all()
        self.assertEqual(districts.count(), 4)
        self.assertListEqual(
            list(districts), [self.fr_nor_bessin, self.fr_nor_perche, self.fr_occ_gard, self.ua_kv_obolon]
        )
        with self.assertRaises(IntegrityError):
            District.objects.create(name="Obolon", region=self.ua_kv)

    def test_localities(self):
        localities = Locality.objects.all()
        self.assertEqual(localities.count(), 5)
        self.assertListEqual(list(localities), [self.bayeux, self.aube, self.essay, self.kherson, self.kiev])
        self.assertEqual(localities[2].region, self.fr_nor)
        self.assertEqual(localities[3].region, self.ua_ks)
        self.assertEqual(localities[4].region, self.ua_kv)
        self.assertIsNone(localities[3].district)
        self.assertIsNone(localities[4].district)
        with self.assertRaises(IntegrityError):
            Locality.objects.create(name="Kherson", region=self.ua_ks)

    def test_streets(self):
        streets = Street.objects.all()
        self.assertEqual(streets.count(), 3)
        self.assertListEqual(list(streets), [self.street2, self.street3, self.street1])
        with self.assertRaises(IntegrityError):
            Street.objects.create(name="Ushakova Avenue", locality=self.kherson)

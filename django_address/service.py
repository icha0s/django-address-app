import abc
from dataclasses import dataclass
from typing import Union
from uuid import UUID

from django.db import transaction

import swapper


class AddressError(Exception):
    pass


@dataclass
class AbstractAddress(metaclass=abc.ABCMeta):
    """Abstract Class describes address information."""

    raw: str = ""
    country: Union[str, int, UUID] = ""
    country_code: str = ""
    region: Union[str, int, UUID] = ""
    region_code: str = ""
    district: Union[str, int, UUID] = ""
    district_code: str = ""
    locality: Union[str, int, UUID] = ""
    postal_code: str = ""
    street: Union[str, int, UUID] = ""
    street_number: str = ""
    apartment: str = ""
    formatted_address: str = ""
    latitude: float = 0
    longitude: float = 0

    def __post_init__(self):
        self.Country = swapper.load_model("django_address", "Country", required=True)
        self.Region = swapper.load_model("django_address", "Region", required=True)
        self.District = swapper.load_model("django_address", "District", required=True)
        self.Locality = swapper.load_model("django_address", "Locality", required=True)
        self.Street = swapper.load_model("django_address", "Street", required=True)
        self.Address = swapper.load_model("django_address", "Address", required=True)

    @abc.abstractmethod
    def save(self, **kwargs):
        raise NotImplementedError


@dataclass
class Address(AbstractAddress):
    @classmethod
    def _get_or_create(cls, model, value, create=True, **kwargs):
        if isinstance(value, (int, UUID)):
            return model.get_or_none(pk=value)
        obj = None
        if value:
            obj = model.objects.filter(name=value, **kwargs).first()
        return model.objects.create(name=value, **kwargs) if obj is None and create else obj

    def get_or_create_country(self, create=True):
        if isinstance(self.country, self.Country):
            return self.country
        if self.country or self.country_code:
            return self._get_or_create(model=self.Country, value=self.country, create=create, code=self.country_code)
        return None

    def get_or_create_region(self, create=True):
        if isinstance(self.region, self.Region):
            return self.region
        if self.region or self.region_code:
            with transaction.atomic():
                if not isinstance(self.country, self.Country) and create:
                    self.country = self.get_or_create_country()
                return self._get_or_create(
                    model=self.Region, value=self.region, create=create, code=self.region_code, country=self.country
                )
        return None

    def get_or_create_district(self, create=True):
        if isinstance(self.district, self.District):
            return self.district
        if self.district or self.district_code:
            with transaction.atomic():
                if not isinstance(self.region, self.Region) and create:
                    self.region = self.get_or_create_region()
                return self._get_or_create(
                    model=self.District, value=self.district, create=create, code=self.district_code, region=self.region
                )
        return None

    def get_or_create_locality(self, create=True):
        if isinstance(self.locality, self.Locality):
            return self.locality
        if self.locality or self.postal_code:
            with transaction.atomic():
                if not isinstance(self.region, self.Region) and create:
                    self.region = self.get_or_create_region()
                if not isinstance(self.district, self.District) and create:
                    self.district = self.get_or_create_district()
                return self._get_or_create(
                    model=self.Locality,
                    value=self.locality,
                    create=create,
                    postal_code=self.postal_code,
                    region=self.region,
                    district=self.district,
                )
        return None

    def get_or_create_street(self, create=True):
        if isinstance(self.street, self.Street):
            return self.street
        if self.street:
            with transaction.atomic():
                if not isinstance(self.locality, self.Locality) and create:
                    self.locality = self.get_or_create_locality()
                return self._get_or_create(model=self.Street, value=self.street, create=create, locality=self.locality)
        return None

    def save(self):
        """Saves address info to django model."""
        with transaction.atomic():
            try:
                self.street = self.get_or_create_street()
                return self.Address.objects.create(
                    locality=self.street.locality,  # noqa
                    street=self.street,
                    raw=self.raw,
                    route=str(self.street),
                    street_number=self.street_number,
                    formatted_address=self.formatted_address,
                    latitude=self.latitude,
                    longitude=self.longitude,
                    apartment=self.apartment,
                )
            except Exception as error:
                raise AddressError from error

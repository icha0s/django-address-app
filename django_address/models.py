import json

from django.db import models
from django.forms.models import model_to_dict
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import swapper


class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects."""

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class AbstractCountryModel(models.Model):
    """Abstract country model."""

    name = models.CharField(_("Name"), max_length=50, unique=True)
    code = models.CharField(_("Code"), max_length=2, blank=True, default="")

    objects = GetOrNoneManager()

    class Meta:
        abstract = True
        ordering = ("name",)
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return "{name}".format(name=self.name or self.code)

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AbstractAdministrativeAreaLevel1Model(models.Model):
    """Abstract administrative area level 1 model (example: State or Region)."""

    name = models.CharField(_("Name"), max_length=150)
    code = models.CharField(_("Code"), max_length=5, blank=True, default="")
    country = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Country"), on_delete=models.PROTECT, verbose_name=_("Country"),
    )

    objects = GetOrNoneManager()

    class Meta:
        abstract = True
        ordering = ("country", "name")
        unique_together = (("name", "country"),)

    def __str__(self):
        country = "{country}".format(country=self.country)
        name = "{name}".format(name=self.name or self.code)
        if country:
            return "{name}, {country}".format(name=name, country=country)
        return name or country

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AbstractAdministrativeAreaLevel2Model(models.Model):
    """Abstract administrative area level 2 model."""

    name = models.CharField(_("Name"), max_length=150)
    code = models.CharField(_("Code"), max_length=5, blank=True, default="")

    objects = GetOrNoneManager()

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        suffix = "{suffix}".format(
            suffix=(
                getattr(self, "region", "")
                or getattr(self, "state", "")
                or getattr(self, "province", "")
                or getattr(self, "canton", "")
            )
        )
        name = "{name}".format(name=self.name or self.code)
        if suffix:
            return "{name}, {suffix}".format(name=name, suffix=suffix)
        return name

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AbstractLocalityModel(models.Model):
    """Abstract locality model."""

    name = models.CharField(_("Name"), max_length=100)
    postal_code = models.CharField(_("Postal code"), max_length=10, blank=True, default="")

    objects = GetOrNoneManager()

    class Meta:
        abstract = True
        ordering = ("name",)
        verbose_name = _("Locality")
        verbose_name_plural = _("Localities")

    def __str__(self):
        suffix = "{suffix}".format(suffix=getattr(self, "district", "") or getattr(self, "county", ""))
        locality = "{name}".format(name=self.name)
        if suffix:
            return "{locality}, {suffix}".format(locality=locality, suffix=suffix)
        return locality

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AbstractStreetModel(models.Model):
    """Abstract street model."""

    locality = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Locality"), on_delete=models.CASCADE, verbose_name=_("Locality")
    )
    name = models.CharField(_("Street name"), max_length=256)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True
        ordering = ("name",)
        unique_together = (("locality", "name"),)
        verbose_name = _("Street")
        verbose_name_plural = _("Streets")

    def __str__(self):
        return "{name}".format(name=self.name)

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


class AbstractAddressModel(models.Model):
    """Abstract address model."""

    locality = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Locality"),
        on_delete=models.CASCADE,
        verbose_name=_("Locality"),
        null=True,
    )
    street = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Street"),
        on_delete=models.CASCADE,
        verbose_name=_("Street"),
        null=True,
    )
    raw = models.CharField(_("Raw"), max_length=256, blank=True, default="")
    route = models.CharField(_("Route"), max_length=256, default="")
    street_number = models.CharField(_("Street number"), max_length=20, blank=True, default="")
    formatted_address = models.CharField(_("Formatted address"), max_length=200, blank=True, default="")
    latitude = models.FloatField(_("Latitude"), blank=True, default=0)
    longitude = models.FloatField(_("Longitude"), blank=True, default=0)
    apartment = models.CharField(_("Apartment"), max_length=10, blank=True, default="")

    objects = GetOrNoneManager()

    class Meta:
        abstract = True
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        if self.formatted_address:
            return self.formatted_address

        locality = "{locality}".format(locality=self.locality)
        route = self.street.name if self.street else self.route
        address = "{route}{street_number}{apartment}".format(
            route=route,
            street_number=", {street_number}".format(street_number=self.street_number) if self.street_number else "",
            apartment=", {apartment}".format(apartment=self.apartment) if self.apartment else "",
        )
        if route and locality:
            return "{address}, {locality}".format(address=address, locality=locality)
        if route:
            return address

        return self.raw

    def save(self, *args, **kwargs):
        if not self.route and self.street:
            self.route = str(self.street)
        if not self.locality and self.street:
            self.locality = self.street.locality
        if not self.formatted_address:
            self.formatted_address = str(self)
        return super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "raw": self.raw,
            "locality": self.locality.to_dict() if self.locality else "",
            "street": self.street.to_dict() if self.street else "",
            "route": self.route,
            "street_number": self.street_number,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "formatted_address": self.formatted_address,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Country(AbstractCountryModel):
    """Country model."""

    class Meta(AbstractCountryModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Country")


class Region(AbstractAdministrativeAreaLevel1Model):
    """Region model."""

    class Meta(AbstractAdministrativeAreaLevel1Model.Meta):
        swappable = swapper.swappable_setting("django_address", "Region")
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class District(AbstractAdministrativeAreaLevel2Model):
    """District model."""

    region = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Region"),
        on_delete=models.CASCADE,
        verbose_name=_("Region"),
        related_name="districts",
    )

    class Meta(AbstractAdministrativeAreaLevel2Model.Meta):
        swappable = swapper.swappable_setting("django_address", "District")
        ordering = ("region", "name")
        unique_together = (("name", "region"),)
        verbose_name = _("District")
        verbose_name_plural = _("Districts")


class Locality(AbstractLocalityModel):
    """Locality model."""

    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    region = models.ForeignKey(
        to=swapper.get_model_name("django_address", "Region"),
        on_delete=models.CASCADE,
        verbose_name=_("Region"),
        related_name="localities",
    )

    district = models.ForeignKey(
        to=swapper.get_model_name("django_address", "District"),
        on_delete=models.CASCADE,
        verbose_name=_("District"),
        related_name="localities",
        blank=True,
        null=True,
    )

    class Meta(AbstractLocalityModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Locality")
        ordering = ("region", "district", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Street(AbstractStreetModel):
    """Street model."""

    class Meta(AbstractStreetModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Street")


class Address(AbstractAddressModel):
    """Address model."""

    class Meta(AbstractAddressModel.Meta):
        swappable = swapper.swappable_setting("django_address", "Address")

    def to_dict(self):
        address = {
            "raw": self.raw,
            "locality": self.locality.to_dict() if self.locality else "",
            "street": self.street.to_dict() if self.street else "",
            "route": self.route,
            "street_number": self.street_number,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "formatted_address": self.formatted_address,
        }

        district = self.locality.district if self.locality else None
        region = self.locality.region if self.locality else None
        country = region if region else None
        if country:
            address.update({"country": country.to_dict()})
        if region:
            address.update({"region": region.to_dict()})
        if district:
            address.update({"district": district.to_dict()})
        return address

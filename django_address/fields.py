from uuid import UUID

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

import swapper

from django_address.service import AddressError


class AddressDescriptor(ForwardManyToOneDescriptor):
    def __set__(self, inst, value):
        self.Address = swapper.load_model("django_address", "Address", required=True)  # noqa
        super().__set__(inst, self.to_python(value))

    def to_python(self, value):

        if value is None:
            return None

        if isinstance(value, (self.Address, int, UUID)):
            return value

        if isinstance(value, dict):
            try:
                address_svc = import_string(
                    getattr(settings, "DJANGO_ADDRESS_SERVICE_CLASS", "django_address.service.Address")
                )
                new_address = address_svc(**value)
                return new_address.save()
            except AddressError:
                raise ValidationError("Invalid address value.")

        raise ValidationError("Invalid address value.")


class AddressField(models.ForeignKey):
    """Address field."""

    description = _("Address")

    def __init__(self, *args, **kwargs):
        kwargs["to"] = swapper.get_model_name("django_address", "Address")
        kwargs["on_delete"] = models.CASCADE
        super(AddressField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False, **kwargs):
        super().contribute_to_class(cls, name, private_only=virtual_only, **kwargs)
        setattr(cls, self.name, AddressDescriptor(self))

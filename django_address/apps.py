from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AddressConfig(AppConfig):
    """Address application."""

    name = "django_address"
    verbose_name = _("Address")

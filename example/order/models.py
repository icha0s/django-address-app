from django.db import models
from django.utils.translation import gettext_lazy as _

from django_address.fields import AddressField


class Order(models.Model):
    """Order model."""

    price = models.DecimalField(_("Price"), max_digits=20, decimal_places=2)
    delivery_address = AddressField(verbose_name=_("Delivery address"), on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return "Order #{pk}, {price}, delivery: {address}".format(
            pk=self.pk, price=self.price, address=self.delivery_address
        )

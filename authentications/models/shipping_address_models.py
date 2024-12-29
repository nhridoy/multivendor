from django.db import models

from core.models import BaseModel


class ShippingAddress(BaseModel):
    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.CASCADE,
        related_name="shipping_addresses",
    )
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - {self.address}"

    class Meta:
        verbose_name_plural = "Shipping Addresses"

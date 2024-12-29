from django.db import models

from core.models import BaseModel


class Cart(BaseModel):
    """Cart model for handling user carts."""

    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.CASCADE,
        limit_choices_to={"role": "user"},
        related_name="carts",
    )
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart({self.user}, {self.product}, {self.quantity})"

    def total_price(self):
        return self.quantity * self.product.price

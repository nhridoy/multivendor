from django.db import models

from core.models import BaseModel


class Order(BaseModel):
    """Order model for managing placed orders."""

    ORDER_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.CASCADE,
        related_name="orders",
        limit_choices_to={"role": "user"},
    )
    shipping_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    shipping_phone = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="pending"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order({self.user}, {self.status}, Total: {self.total_price})"


class OrderItem(BaseModel):
    """OrderItem model for handling individual items in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(
        "authentications.User",
        on_delete=models.CASCADE,
        related_name="order_items",
        limit_choices_to={"role": "seller"},
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Store the price at the time of order

    def __str__(self):
        return f"OrderItem({self.order}, {self.product}, Quantity: {self.quantity})"

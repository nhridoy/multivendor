from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CompressedImageField


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="sub_categories"
    )
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")

    def __str__(self):
        return self.name


class Product(BaseModel):
    user = models.ForeignKey(
        "authentications.User", on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = CompressedImageField(
        quality=75,
        width=1920,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

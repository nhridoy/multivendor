# Generated by Django 5.1.2 on 2024-12-29 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_remove_order_shipping_address_order_address_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="address",
            new_name="shipping_address",
        ),
    ]
# Generated by Django 5.1.2 on 2024-12-29 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_rename_address_order_shipping_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="status",
        ),
    ]

# Generated by Django 5.1.2 on 2024-12-29 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentications", "0003_alter_userinformation_phone_number"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ShippingAddress",
        ),
    ]
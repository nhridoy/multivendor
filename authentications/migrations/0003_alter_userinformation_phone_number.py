# Generated by Django 5.1.2 on 2024-12-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentications", "0002_shippingaddress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinformation",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Phone Number"
            ),
        ),
    ]

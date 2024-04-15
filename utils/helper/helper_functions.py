import os
import random
from datetime import datetime

from django.core.validators import RegexValidator

# phone number validate
phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
                                 "The phone number provided is invalid")


def content_file_path(instance, filename):
    model_name = instance.__class__.__name__.replace("Model", "")
    ext = filename.split(".")[-1]
    current_date = datetime.now()
    date_path = current_date.strftime("%Y-%m-%d")
    unique_filename = f"{instance}-{instance.pk}.{ext}"
    return os.path.join(model_name, date_path, unique_filename)

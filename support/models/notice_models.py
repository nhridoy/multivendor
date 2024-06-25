from django.db import models

from core.models import BaseModel
from utils.helper import content_file_path


class Notice(BaseModel):
    user = models.ForeignKey(
        "authentications.User", on_delete=models.CASCADE, related_name="notices"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to=content_file_path, blank=True, null=True)

    def __str__(self):
        return self.title

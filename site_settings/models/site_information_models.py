from autoslug import AutoSlugField
from django.db import models

from core.models import BaseModel
from utils.helper import content_file_path


class SiteInformation(BaseModel):
    """
    Model for storing site information, so that these can change without touching the code.
    """

    logo = models.ImageField(upload_to=content_file_path)
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    reddit = models.URLField(blank=True, null=True)
    tumblr = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    slack = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

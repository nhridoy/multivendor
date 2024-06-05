from django.db import models

# Create your models here.
from authentications.models import User
from core.models import BaseModel


class Notifications(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_user", null=True, blank=True)
    title = models.CharField(max_length=200, )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    groups_notification = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Groups(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=255)
    group_participants = models.ManyToManyField(User, related_name="group_participants")

    def __str__(self):
        return self.name


class NotificationsGroup(BaseModel):
    notification = models.ForeignKey(Notifications, on_delete=models.CASCADE, related_name="notification_group")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="group_notification")

    def __str__(self):
        return self.group.name

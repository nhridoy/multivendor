from authentications.models import User
from core.models import *


class NoticeType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=255)


# Create your models here.
class Notice(BaseModel):
    type = models.ForeignKey(NoticeType, on_delete=models.CASCADE, related_name="notice_type")
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="notice_author")


class NoticeRecipient(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notice_recipient_user")
    notice = models.ForeignKey(Notice, on_delete=models.PROTECT, related_name="notice_recipient")
    read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)

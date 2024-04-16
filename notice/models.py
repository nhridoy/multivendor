from authentications.models import User
from core.models import *


# Create your models here.
class Notice(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)


class NoticeRecipient(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)

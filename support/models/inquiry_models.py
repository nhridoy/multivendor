from django.db import models

from core.models import BaseModel

# Create your models here.


class Inquiry(BaseModel):
    user = models.ForeignKey(
        "authentications.User", on_delete=models.CASCADE, related_name="inquiries"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Inquiries"


class InquiryAnswer(BaseModel):
    inquiry = models.OneToOneField(
        Inquiry, on_delete=models.CASCADE, related_name="answer"
    )
    answer = models.TextField()
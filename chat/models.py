from django.db import models
from core import settings
from core.models import BaseModel
from utils.helper import content_file_path


class ChatRoom(BaseModel):
    name = models.CharField(max_length=256)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms_participants')
    room_id = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class ChatLog(BaseModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages_room')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.room


class ChatText(BaseModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_texts_log')
    content = models.CharField(max_length=1024)

    def __str__(self):
        return self.room


class ChatImage(BaseModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_images_log')
    attachment = models.FileField(upload_to=content_file_path)

    def __str__(self):
        return self.room

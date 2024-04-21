from rest_framework.viewsets import ModelViewSet

from notifications.models import Notifications
from notifications.serializers import NotificationSerializer


class NotificationsView(ModelViewSet):
    queryset = Notifications.objects.select_related()
    serializer_class = NotificationSerializer




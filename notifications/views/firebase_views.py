from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from notifications.serializers import PushNotificationSerializer
from utils.modules.firebase_cloud_messaging import FCMNotificationSender


class FcmAPIView(ViewSet):
    permission_classes = []
    serializer_class = PushNotificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        firebase = FCMNotificationSender(title=data.get("title"), body=data.get("body"),
                                         image=data.get("image"))  # Initialize the FCMNotificationSender class
        if firebase.send_single_notification():
            return Response({"message": "Notification sent!"})
        return Response({"message": "An error occurred while sending notification."},
                        status=status.HTTP_400_BAD_REQUEST)

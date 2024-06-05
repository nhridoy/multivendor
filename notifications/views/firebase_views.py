import json
from firebase_admin import credentials
from google.oauth2 import service_account
import argparse
import google.auth.transport.requests
import firebase_admin
from fcm_django.models import FCMDevice

import requests
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from notifications.serializers import PushNotificationSerializer
from utils.modules.firebase_cloud_messaging import FCMNotificationSender

#
PROJECT_ID = 'test-e8e8c'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """
    credentials = service_account.Credentials.from_service_account_file(
        'google-services.json', scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


def _send_fcm_message(fcm_message):
    """Send HTTP request to FCM with given message.

    Args:
      fcm_message: JSON object that will make up the body of the request.
    """
    # [START use_access_token]
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
    }
    # [END use_access_token]
    resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

    if resp.status_code == 200:
        print('Message sent to Firebase for delivery, response:')
        print(resp.text)
    else:
        print('Unable to send message to Firebase')
        print(resp.text)


class FcmAPIView(ViewSet):
    permission_classes = []
    serializer_class = PushNotificationSerializer

    def post(self, request, *args, **kwargs):
        reg_id = FCMDevice.objects.all().first().registration_id
        _send_fcm_message(
            {
                "message": {
                    "token": "fPxDomdBozLhKEusqJx2VQ:APA91bH9SDk0z7Z9zXzDMW3UcgWZet1HK52C0dL2-AnVOvvud7fP48jSx1iK35-AedrnBdEdCPAVDX12zGub3jgEHGkn948GrpUtQzyyw3domVfpS1NQMGnM4ln_x083WFnbQ503kG5U",
                    "notification": {
                        "body": "This is an FCM notification message!",
                        "title": "FCM Message"
                    },
                    "data": {
                        "Nick": "Mario",
                        "Room": "PortugalVSDenmark"
                    }
                }
            }
        )
        return Response({"message": "Notification sent!"})

# class FcmAPIView(ViewSet):
#     permission_classes = []
#     serializer_class = PushNotificationSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.data
#         firebase = FCMNotificationSender(title=data.get("title"), body=data.get("body"),
#                                          image=data.get("image"))  # Initialize the FCMNotificationSender class
#         if firebase.send_single_notification():
#             return Response({"message": "Notification sent!"})
#         return Response({"message": "An error occurred while sending notification."},
#                         status=status.HTTP_400_BAD_REQUEST)

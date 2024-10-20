from rest_framework import mixins, permissions, response, viewsets
from rest_framework.decorators import action

from authentications.models import User
from authentications.serializers import PersonalProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PersonalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ["get", "put", "patch"]

    def get_queryset(self):
        return User.objects.select_related(
            "user_information",
            "user_information__country",
            "user_information__province",
            "user_information__city",
        )

    def get_object(self):
        return self.get_queryset().get(id=self.request.user.id)

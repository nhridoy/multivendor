from rest_framework import mixins, permissions, response, viewsets
from rest_framework.decorators import action

from authentications.models import User
from authentications.serializers import PersonalProfileSerializer


class ProfileViewSet(viewsets.GenericViewSet):
    serializer_class = PersonalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.select_related(
            "user_information",
            "user_information__country",
            "user_information__province",
            "user_information__city",
        )

    @action(detail=False, methods=["get", "put", "patch"])
    def profile(self, request):
        user = self.get_queryset().get(id=request.user.id)
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return response.Response(serializer.data)
        elif request.method in ["PUT", "PATCH"]:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)

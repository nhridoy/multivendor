from rest_framework import mixins, permissions, response, viewsets
from rest_framework.decorators import action

from authentications.models import User
from authentications.serializers import PersonalProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PersonalProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.select_related(
        "user_information",
        "user_information__language",
        "user_information__country",
        "user_information__province",
        "user_information__city",
    )
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        # if self.request.user.role == "nanny":
        #     return self.queryset.prefetch_related(
        #         "nanny_information",
        #         "nanny_information__category",
        #         "nanny_information__preferred_provinces",
        #         "nanny_information__preferred_cities",
        #         "nanny_information__preferred_classes",
        #         "nanny_information__preferred_age_groups",
        #         "nanny_information__nanny_certification",
        #     )
        return self.queryset

    def get_object(self):
        return self.get_queryset().get(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

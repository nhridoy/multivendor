from django.db.utils import IntegrityError
from rest_framework import exceptions, generics, permissions, response, viewsets

from support.models import Inquiry, InquiryAnswer
from support.serializers import InquiryAnswerSerializer, InquirySerializer
from utils.extensions.permissions import IsAdmin


class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"
    http_method_names = ["get", "post"]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return (
                Inquiry.objects.all()
                .select_related("answer", "user__user_information")
                .order_by("-created_at")
            )
        return (
            Inquiry.objects.filter(user=self.request.user)
            .select_related("answer", "user__user_information")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class InquiryAnswerView(generics.CreateAPIView):
    serializer_class = InquiryAnswerSerializer
    permission_classes = (IsAdmin,)
    queryset = InquiryAnswer.objects.all()

    def perform_create(self, serializer):
        try:
            return serializer.save(inquiry_id=self.kwargs.get("id"))
        except IntegrityError as e:
            raise exceptions.PermissionDenied(detail="Already Answered") from e

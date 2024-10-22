from django.db.utils import IntegrityError
from rest_framework import exceptions, generics, permissions, response, viewsets

from support.models import Inquiry, InquiryAnswer
from support.serializers import InquiryAnswerSerializer, InquirySerializer
from utils.extensions.permissions import IsAdmin, IsAdminOrReadOnly


class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"
    http_method_names = ["get", "post"]
    queryset = (
        Inquiry.objects.select_related("inquiry_answers", "user__user_information")
        .all()
        .order_by("-created_at")
    )

    def get_queryset(self):
        if self.request.user.role == "admin":
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class InquiryAnswerView(generics.ListCreateAPIView):
    serializer_class = InquiryAnswerSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    )
    queryset = InquiryAnswer.objects.all()

    def get_queryset(self):
        inquiry_id = self.kwargs.get("id")
        if self.request.user.role == "admin":
            return self.queryset.filter(inquiry_id=inquiry_id)
        return self.queryset.filter(
            inquiry_id=inquiry_id, inquiry__user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(inquiry_id=self.kwargs.get("id"), user=self.request.user)

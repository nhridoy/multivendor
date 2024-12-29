from rest_framework import permissions, viewsets

from authentications.models import ShippingAddress
from authentications.serializers import ShippingAddressSerializer
from utils.extensions.permissions import IsOwnerOrReadOnly


class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

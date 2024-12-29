from rest_framework import permissions, response, status, viewsets

from orders.models import Cart, Order, OrderItem
from orders.serializers import (
    OrderDetailSerializer,
    OrderItemDetailSerializer,
    OrderItemSerializer,
    OrderSerializer,
)
from utils.extensions.permissions import IsSellerOrAdmin


class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling orders, including converting cart items to an order.
    """

    queryset = Order.objects.prefetch_related("items", "items__product")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for handling order items.
    """

    queryset = (
        OrderItem.objects.select_related("product").prefetch_related("order").all()
    )
    permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderItemDetailSerializer
        return OrderItemSerializer

    def get_queryset(self):
        if self.request.user.role == "admin":
            return self.queryset
        return self.queryset.filter(seller=self.request.user)

from rest_framework import decorators, permissions, response, viewsets

from orders.models import Cart
from orders.serializers import CartSerializers
from utils.extensions.permissions import IsOwnerOrReadOnly


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializers
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "delete"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CartSerializers(queryset, many=True)
        total_price = sum(cart.total_price() for cart in queryset)
        return response.Response(
            {"total_price": total_price, "cart_items": serializer.data}
        )

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @decorators.action(detail=False, methods=["get"], url_path="increase-quantity")
    def increase_quantity(self, request):
        user = request.user
        item_id = request.query_params.get("item_id")
        cart = Cart.objects.filter(user=user, id=item_id).first()
        if cart:
            cart.quantity += 1
            cart.save(update_fields=["quantity"])
            return response.Response({"message": "Increase quantity successfully"})
        return response.Response({"message": "Cart not found"}, status=404)

    @decorators.action(detail=False, methods=["get"], url_path="decrease-quantity")
    def decrease_quantity(self, request):
        user = request.user
        item_id = request.query_params.get("item_id")
        cart = Cart.objects.filter(user=user, id=item_id).first()
        if cart:
            cart.quantity -= 1
            cart.save(update_fields=["quantity"])
            return response.Response({"message": "Decrease quantity successfully"})
        return response.Response({"message": "Cart not found"}, status=404)

from django.db import transaction
from rest_framework import exceptions, serializers

from orders.models import Cart, Order, OrderItem
from product.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "seller", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "total_price",
            "status",
            "created_at",
            "updated_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        cart_items = Cart.objects.filter(user=user).select_related(
            "product", "product__user"
        )
        if not cart_items.exists():
            raise exceptions.ValidationError("Your cart is empty.")

        # Calculate total price and create the order

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(total_price=total_price, **validated_data)

        # Create OrderItems and associate them with the order
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                seller=cart_item.product.user,
                total_price=cart_item.total_price(),
            )

        # Clear the user's cart
        cart_items.delete()
        return order


class OrderDetailSerializer(OrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ["items"]
        read_only_fields = OrderSerializer.Meta.read_only_fields + ["items"]

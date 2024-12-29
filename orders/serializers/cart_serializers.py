from rest_framework import serializers

from orders.models import Cart


class CartSerializers(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ("user",)

    def get_total_price(self, obj):
        return obj.total_price()

    def create(self, validated_data):
        # If the user has the same product in the cart, update the quantity
        user = validated_data.get("user")
        product = validated_data.get("product")
        quantity = validated_data.get("quantity", 1)
        cart = Cart.objects.filter(user=user, product=product).first()
        if cart:
            cart.quantity += quantity
            cart.save(update_fields=["quantity"])
            return cart
        return super().create(validated_data)

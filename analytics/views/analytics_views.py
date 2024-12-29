from django.db.models import Sum
from rest_framework import permissions, response, viewsets

from authentications.models import User
from orders.models import OrderItem
from product.models import Product
from utils.extensions.permissions import IsSellerOrAdmin


class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSellerOrAdmin]

    def list(self, request):
        data = {}
        if request.user.role == "seller":
            data = {
                "total_sales": OrderItem.objects.filter(seller=request.user).aggregate(
                    total_sales=Sum("total_price")
                )["total_sales"],
                "total_orders": OrderItem.objects.filter(seller=request.user).count(),
                "total_products": Product.objects.filter(user=request.user).count(),
                "total_customers": OrderItem.objects.filter(seller=request.user)
                .values("order__user")
                .distinct()
                .count(),
            }
        elif request.user.role == "admin":
            data = {
                "total_sales": OrderItem.objects.aggregate(
                    total_sales=Sum("total_price")
                )["total_sales"],
                "total_orders": OrderItem.objects.count(),
                "total_products": Product.objects.count(),
                "total_customers": User.objects.filter(role="user").count(),
                "total_sellers": User.objects.filter(role="seller").count(),
            }

        return response.Response(data)

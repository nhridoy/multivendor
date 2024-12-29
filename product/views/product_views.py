from rest_framework import permissions, viewsets

from product.models import Category, Product, SubCategory
from product.serializers import (
    CategorySerializer,
    ProductSerializer,
    SubCategorySerializer,
)
from utils.extensions.permissions import IsAdminOrReadOnly, IsSeller, IsSellerOrAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ["category", "sub_category", "user"]

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated(), IsSeller()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsSellerOrAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "seller":
            return self.queryset.filter(user=self.request.user)
        start_price = self.request.query_params.get("start_price")
        end_price = self.request.query_params.get("end_price")
        if start_price and end_price:
            return self.queryset.filter(price__range=(start_price, end_price))
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from django.urls import path
from rest_framework.routers import DefaultRouter

from product.views.product_views import (
    CategoryViewSet,
    ProductViewSet,
    SubCategoryViewSet,
)

router = DefaultRouter()
#  register modelViewSets for articles
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"sub-categories", SubCategoryViewSet, basename="sub-categories")
router.register(r"", ProductViewSet, basename="products")

urlpatterns = []
urlpatterns += router.urls

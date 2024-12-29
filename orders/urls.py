from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import CartViewSet, OrderItemViewSet, OrderViewSet

router = DefaultRouter()
#  register modelViewSets
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"order-item", OrderItemViewSet, basename="order-item")
router.register(r"", OrderViewSet, basename="order")

urlpatterns = []
urlpatterns += router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import CartViewSet, OrderViewSet

router = DefaultRouter()
#  register modelViewSets
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"order", OrderViewSet, basename="order")

urlpatterns = []
urlpatterns += router.urls

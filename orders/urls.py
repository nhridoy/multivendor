from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import CartViewSet

router = DefaultRouter()
#  register modelViewSets
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = []
urlpatterns += router.urls

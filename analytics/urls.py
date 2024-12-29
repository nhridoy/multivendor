from django.urls import path
from rest_framework.routers import DefaultRouter

from analytics.views import AnalyticsViewSet

router = DefaultRouter()
#  register modelViewSets
router.register(r"", AnalyticsViewSet, basename="analytics")

urlpatterns = []
urlpatterns += router.urls

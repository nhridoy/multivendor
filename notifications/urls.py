from django.urls import path
from rest_framework.routers import DefaultRouter

from notifications.views import NotificationsView

router = DefaultRouter()

router.register('notifications', NotificationsView, basename='notifications')

urlpatterns = [

]
urlpatterns += router.urls

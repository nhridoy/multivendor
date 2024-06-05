from django.urls import path
from rest_framework.routers import DefaultRouter
from notice.views import NoticeView, NoticeTypeView

router = DefaultRouter()
#  register modelviewset for notice and notice type
router.register('notice-type', NoticeTypeView, basename='notice_type')
router.register('notice', NoticeView, basename='notice')

urlpatterns = [

]
urlpatterns += router.urls

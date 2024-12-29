from django.urls import path
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
#  register modelViewSets for articles
# router.register("categories", ArticleCategoryView, basename="article-categories")

urlpatterns = []
urlpatterns += router.urls

from rest_framework.routers import DefaultRouter
from options.views import (
    CityView,
    CountryView,
    LanguageView,
    ProvinceView,
)

router = DefaultRouter()
router.register(r"admin/language", LanguageView, basename="admin/language")
router.register(r"admin/province", ProvinceView, basename="admin/province")
router.register(r"admin/city", CityView, basename="admin/city")
router.register(r"admin/country", CountryView, basename="admin/country")

urlpatterns = [

]
urlpatterns += router.urls

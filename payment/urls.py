from payment_management.views import GetSavedCardViewSet, MakePaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"make-payment", MakePaymentViewSet, basename="make-payment")
router.register(r"get-saved-cards", GetSavedCardViewSet, basename="get-saved-cards")


urlpatterns = []
urlpatterns += router.urls

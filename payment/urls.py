from rest_framework.routers import DefaultRouter

from payment.views import (
    GetSavedCardViewSet,
    MakePaymentViewSet,
    OrderViewSet,
    PaymentViewSet,
)

router = DefaultRouter()

# Authorize Payment
router.register(r"make-payment", MakePaymentViewSet, basename="make-payment")
router.register(r"get-saved-cards", GetSavedCardViewSet, basename="get-saved-cards")

# Toss Payment
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"complete", PaymentViewSet, basename="complete")


urlpatterns = []
urlpatterns += router.urls

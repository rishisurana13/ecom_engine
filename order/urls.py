from django.urls import include, path
from rest_framework.routers import DefaultRouter
from order.views import LineItemViewSet, CheckoutListAPIView,OrderModelViewSet
from django.urls import path




router = DefaultRouter()
router.register(r"cart", LineItemViewSet),
router.register(r"orders", OrderModelViewSet),





urlpatterns = [
   
    path("", include(router.urls)),
    path("checkout/", CheckoutListAPIView.as_view(), name='checkout-view'),
	# path("orders/", OrderListAPIView.as_view(), name="order-list"),
	# path("orders/<int:pk>/", OrderRetrieveUpdateAPIView.as_view(), name="order-detail"),
	# # path("orders/<int:pk>/final_payment/", OrderAddFinalPaymentRetrieveUpdateAPIView.as_view(), name="order-final-payment"),

]
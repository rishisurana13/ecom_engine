from django.urls import include, path

from payment.views import PaymentRetrieveUpdateAPIView,PaymentListAPIView




urlpatterns = [
   
  
	path("payments/<int:pk>/", PaymentRetrieveUpdateAPIView.as_view(), name="payment-detail"),
	path("payments/", PaymentListAPIView.as_view(), name="payment-list"),

]
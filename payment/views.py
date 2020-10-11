from rest_framework.generics import RetrieveUpdateAPIView,ListAPIView
from payment.models import Payment
from payment.serializers import PaymentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import stripe

class PaymentRetrieveUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated ]
	authentication_classes = (TokenAuthentication,)
	
	def get_queryset(self):
		account = self.request.user.account
		return self.queryset.filter(order__account=account.id)

class PaymentListAPIView(ListAPIView):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated ]
	authentication_classes = (TokenAuthentication,)
	
	def get_queryset(self):
		account = self.request.user.account
		return self.queryset.filter(order__account=account.id)


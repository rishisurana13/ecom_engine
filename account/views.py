
from account.serializers import AccountSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from account.models import Account
from permissions.permissions import IsAdminUserOrReadOnly,AdminCanReadOnly, IsUserAndAdminCanReadOnly
from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

class AccountListAPIView(ListAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer
	permission_classes = [AdminCanReadOnly]

	

class AccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer
	permission_classes = [IsAuthenticated ]
	authentication_classes = (TokenAuthentication,)

	def get_object(self):
		"""Retrieve and return user"""
		return self.request.user.account

	



	


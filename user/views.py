from rest_framework import generics, authentication, permissions
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer,ChangePasswordSerializer, UserLoginSerializer
from user.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 


class CreateUserView(generics.CreateAPIView):
	"""Create a new user in the system"""

	serializer_class = UserLoginSerializer


class CreateTokenView(generics.CreateAPIView, ObtainAuthToken,):
	"""Create  new auth token for user """

	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		user = User.objects.get(email=user)
		cart = user.account.orders.filter(status='checkout')
		total = 0
		for order in cart:
			for li in order.line_items.all():
				total += li.quantity 
		return Response({'token': token.key,
						'user': {
								 'first_name':user.first_name,
								 'last_name': user.last_name,
								 'email':user.email,
								 'cart_length':total
								 }
						})

class ManageUserView(generics.RetrieveUpdateAPIView):
	""" Manage auth user"""

	serializer_class = UserSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)


	def get_object(self):
		"""Retrieve and return user"""
		return self.request.user

class Logout(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	def get(self, request, format=None):
		# simply delete the token to force a login
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
		"""
		An endpoint for changing password.
		"""
		serializer_class = ChangePasswordSerializer
		authentication_classes = (authentication.TokenAuthentication,)

		permission_classes = (permissions.IsAuthenticated,)

		def get_object(self, queryset=None):
			obj = self.request.user
			return obj

		def update(self, request, *args, **kwargs):
			self.object = self.get_object()
			serializer = self.get_serializer(data=request.data)

			if serializer.is_valid():
			# Check old password
				if not self.object.check_password(serializer.data.get("old_password")):
					return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
				# set_password also hashes the password that the user will get
			
				self.object.set_password(serializer.data.get("new_password"))
				self.object.save()
				response = {
				'status': 'success',
				'code': status.HTTP_200_OK,
				'message': 'Password updated successfully',
				'data': []
				}

				return Response(response)

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.

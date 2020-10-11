from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
	"""serializer for the users object"""
	account = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = get_user_model()
		fields = ('email','first_name','last_name','account')
		read_only_fields = ('email', 'account', 'first_name', 'last_name')
		extra_kwargs = {
			'password': {'write_only': True,'min_length':5}
		}


	def create(self,validated_data):
		"""Create a new user with encypted password and run it"""
		return get_user_model().objects.create_user(**validated_data)

	def update(self,instance, validated_data):
		"""update a user, setting pw correctly and returning it"""
		password = validated_data.pop('password', None)
		user = super().update(instance, validated_data)

		if password:
			user.set_password(password)
			user.save()
		return user


class UserLoginSerializer(serializers.ModelSerializer):
	"""serializer for the users object"""
	account = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = get_user_model()
		fields = ('first_name','last_name','email','password','account')
		extra_kwargs = {
			'password': {'write_only': True,'min_length':5}
		}



	def create(self,validated_data):
		"""Create a new user with encypted password and run it"""
		return get_user_model().objects.create_user(**validated_data)

	def update(self,instance, validated_data):
		"""update a user, setting pw correctly and returning it"""
		password = validated_data.pop('password', None)
		user = super().update(instance, validated_data)

		if password:
			user.set_password(password)
			user.save()
		return user


class AuthTokenSerializer(serializers.Serializer):
	"""Serializer for the user auth object"""
	
	email = serializers.CharField()
	password = serializers.CharField(
		style={'input_type':'password'},
		trim_whitespace=False
		)
	def validate(self,attrs):
		"""Validate and auth user"""
		email = attrs.get('email')
		password = attrs.get('password')

		user = authenticate(
				request=self.context.get('request'),
				username=email,
				password=password,

			)
		if not user:
			msg = _('Unable to authenticate with provided credentials')
			raise serializers.ValidationError(msg,code='authentication')

		attrs['user'] = user
		return attrs
 

class ChangePasswordSerializer(serializers.Serializer):
	model = settings.AUTH_USER_MODEL

	"""
	Serializer for password change endpoint.
	"""
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)






		

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# from account.models import Account
from django.db import models

class UserManager(BaseUserManager):

	def create_user(self,email,password=None,**extra_fields):

		if not email:
			raise ValueError('Users must have an email address')
		email = email.lower()
		user = self.model(email=self.normalize_email(email),**extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self,email,password):

		user = self.create_user(email,password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255,unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	# account = models.ForeignKey(Account, on_delete=models.CASCADE)
	objects = UserManager()

	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.email 

# Create your models here.

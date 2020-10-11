from django.db import models
from django.conf import settings


class Account(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	city = models.CharField(max_length=100)


	def __str__(self):
		return self.user.first_name + self.user.last_name









	








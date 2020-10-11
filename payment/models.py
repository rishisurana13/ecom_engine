from django.db import models
from order.models import Order

STATUS_CHOICES = (
	("checkout", "Checkout",),
	("success", "Success"),
	("failure","Failure"),
	("refunded","Refunded")
	)

class Payment(models.Model):

	amount = models.FloatField()
	intent_key = models.CharField(max_length=200, blank=True)
	intent_secret = models.CharField(max_length=200, blank=True)
	status = models.CharField(max_length=20,default='checkout')
	order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)	

	def __str__(self):
		return self.intent_key

from django.db import models


FILE_TYPE_CHOICES = (
	("necklace","Necklace"),
	("earrings","Earrings"),
	("bangle", "Bangle"),
	("bracelet", "Bracelet")
	)

class Product(models.Model):
	title = models.CharField(max_length=164, unique=True)
	gold_wt = models.FloatField() 
	diamond_wt = models.FloatField()
	price = models.FloatField()
	product_type = models.CharField(max_length=164,choices=FILE_TYPE_CHOICES)
	discount = models.DecimalField(max_digits=3,decimal_places=2,blank=True) 
	quantity = models.PositiveIntegerField(blank=True,null=True)
	description = models.TextField(blank=True)
	image_url = models.URLField(max_length=300,blank=True)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def final_price(self):
		if self.discount > 0 and self.discount < 1:
			return self.price - (self.price * self.discount)
		else:
			return self.price

	def __str__(self):
		return self.title








	











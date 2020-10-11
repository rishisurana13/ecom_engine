from django.db import models
from product.models import Product
from account.models import Account


STATUS_CHOICES = (
	('checkout', 'Checkout'),
	('gold_paid', 'Gold_paid'),
	('success', 'Success'),
	('failure', 'Failure'),
	('refunded', 'Refunded'),
	)

class Order(models.Model):
	account = models.ForeignKey(Account, related_name='orders', on_delete=models.CASCADE)
	status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='checkout')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)	
	
	def order_value(self):
		cv = 0
		if len(self.line_items.all()) > 0:
			for line_item in self.line_items.all():
				cv += (line_item.product.final_price()*line_item.quantity)
		
		cv = round(cv,2) 
		return float(cv)

	def first_payment_amount(self):
		payment_amount = 0.0
		gold_rate = 5500 # gold rate per 1 gram
		for li in self.line_items.all():
			if li.product.gold_wt != 0.0:
				payment_amount += (li.product.gold_wt * gold_rate*li.quantity)
			else:
				payment_amount += (li.product.final_price()*0.3*quantity)
		return payment_amount

	def final_payment_amount(self):
		total_paid = 0.0
		amount_due = 0.0
		for payment in self.payments.all():
			total_paid += payment.amount
		amount_due = self.order_value() - self.first_payment_amount()
		return amount_due

	def __str__(self): 
		return str(self.account) + str(self.id)


class LineItem(models.Model):
	
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	order = models.ForeignKey(Order,  related_name='line_items',on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id) + ' ' + self.product.title  


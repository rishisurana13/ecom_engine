from django.contrib import admin
from order.models import Order, LineItem

admin.site.register(Order)
admin.site.register(LineItem)
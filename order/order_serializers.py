from product.serializers import ProductSerializer
from order.models import Order
from order.line_item_serializers import LineItemSummarySerializer
from rest_framework import serializers
from payment.serializers import PaymentSummarySerializer

class OrderSerializer(serializers.ModelSerializer):
	
	# account = serializers.PrimaryKeyRelatedField(read_only=True)
	order_value = serializers.FloatField(read_only=True)
	line_items = LineItemSummarySerializer(read_only=True,many=True)
	payments = PaymentSummarySerializer(read_only=True,many=True)
	amount_due = serializers.SerializerMethodField()


	class Meta:
		model = Order
		fields  = ['id','order_value','first_payment_amount','status','url','line_items','payments','amount_due']
		
	

	def get_amount_due(self,obj):
		# payment is created upon instance creation
		if len(obj.payments.all()) == 1:
			if obj.payments.all()[0].status == 'checkout' or obj.payments.all()[0].status == 'failure' :
				return obj.first_payment_amount()
			else:
				return obj.final_payment_amount()
		elif(len(obj.payments.all()) == 2):
			return obj.final_payment_amount()
		else:
			return obj.first_payment_amount() ## this is a placeholder remove this block after order filtering






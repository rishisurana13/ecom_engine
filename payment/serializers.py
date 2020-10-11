from rest_framework import serializers
from payment.models import Payment

class PaymentSerializer(serializers.ModelSerializer):

	order = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Payment
		fields = ['id','order','amount', 'intent_key', 'intent_secret','url',]

class PaymentSummarySerializer(PaymentSerializer):

	order = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
	class Meta:
		model = Payment
		fields = ['amount','intent_secret','status']
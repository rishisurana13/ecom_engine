from rest_framework import serializers
from account.models import Account
from user.serializers import UserSerializer




	

class AccountSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False, read_only=True)
	# orders = OrderSummarySerializer(many=True,read_only=True)

	class Meta:

		model = Account
		fields = ['id', 'user','city', 'user_id', ]




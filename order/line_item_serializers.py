
from rest_framework import serializers
from product.serializers import ProductSerializer
from order.models import LineItem, Order



class AttrPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        account = self.context['request'].user.account
        queryset = Order.objects.filter(account=account).filter(status='checkout')
        return queryset

class LineItemSerializer(serializers.ModelSerializer):

	total_product_price = serializers.SerializerMethodField()
	base_product_price = serializers.SerializerMethodField()
	product_title = serializers.SerializerMethodField()
	product_image_url = serializers.SerializerMethodField()
	product_id = serializers.SerializerMethodField()
	order = AttrPKField()

	class Meta:
		model = LineItem
		fields = ['product','product_id','product_title', 'quantity', 'url','product_image_url', 'total_product_price', 'base_product_price', 'order']	

	def get_product_title(self, obj):
		return obj.product.title

	def get_base_product_price (self,obj):
		return obj.product.price

	def get_total_product_price(self,obj):
		# print(self.data)
		return obj.product.final_price() * obj.quantity
	def get_product_image_url(self,obj):
		return obj.product.image_url

	def get_product_id(self, obj):
		return obj.product.id


class LineItemSummarySerializer(LineItemSerializer):

	class Meta:
		model = LineItem
		fields = ['product_title','product_id','order', 'quantity','product_image_url', 'total_product_price', 'base_product_price','url']



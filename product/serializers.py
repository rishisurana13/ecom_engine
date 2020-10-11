from rest_framework import serializers

from product.models import Product




class ProductSerializer(serializers.ModelSerializer): 
	
	
	class Meta:
		model = Product
		fields = ['id', 'title','discount','description','price','final_price', 'quantity', 'product_type','gold_wt','diamond_wt', 'url','image_url']
		
	def validate(self, data):
		product_type = data['product_type']
		quantity = data['quantity']
		discount = float(data['discount'])
		if product_type[0] =='p': 
			if quantity == None:
				raise serializers.ValidationError('Physical Products MUST have a set quantity')
			
			if int(quantity) == 0:
				data['available'] = False
			else:
				data['available'] = True

		if discount > 1 or discount < 0:
			raise serializers.ValidationError('Discount can only be a value between 0 and 1.')
		
		return data

	

class ProductSummarySerializer(ProductSerializer):

	class Meta:
		model = Product
		fields = ['id','title','discount','final_price','url','product_type','image_url']




		





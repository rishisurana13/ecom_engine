from order.line_item_serializers import LineItemSerializer, LineItemSummarySerializer
from order.order_serializers import OrderSerializer
from rest_framework.generics import RetrieveUpdateAPIView,ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers

from order.models import LineItem
from permissions.permissions import IsAccountAndAdminCanReadOnly, IsAccountAndAdminCanReadOnlyCart, DeleteNotAllowed
# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated
from order.models import Order
import stripe
import dotenv
import os
from payment.models import Payment
from product.models import Product

path = '.env'
env_file = dotenv.load_dotenv(dotenv_path=path)
stripe.api_key = os.getenv("STRIPE_API_KEY_TEST")

class LineItemViewSet(ModelViewSet):
	queryset = LineItem.objects.all()
	serializer_class = LineItemSummarySerializer
	permission_classes = [ IsAuthenticated,]
	authentication_classes = (TokenAuthentication,)

	def get_serializer_class(self):
		summary_list = ('retrieve','list')
		if self.action in summary_list:
			return LineItemSummarySerializer
		else:
			return LineItemSerializer

	def get_queryset(self):
		return self.queryset.filter(order__status='checkout')

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


	def create(self, request, *args, **kwargs):
		orders = Order.objects.all().filter(account=self.request.user.account,status='checkout')
		f_d = request.data.copy()
		prod_targ = Product.objects.get(id=int(f_d["product"]))
		li_quant = int(f_d["quantity"])
		prod_quant = prod_targ.quantity

		if int(prod_quant) < int(li_quant):
			raise serializers.ValidationError(f"Failed to Create: Only {prod_quant} item(s) left in stock.")

		if len(orders) == 1:
			for order in orders:
				order = Order.objects.get(pk=order.id)
				f_d["order"] = order.id

		elif len(orders) == 0:
			order = Order.objects.create(account=self.request.user.account,status='checkout',)
			f_d["order"] = order.id

			
		if len(orders) == 1:
			for order in orders:
				for li in order.line_items.all():
					if li.product.id == int(f_d["product"]):
						instance = LineItem.objects.get(id=li.id)
						instance.quantity = instance.quantity + int(f_d["quantity"]) 
						instance.save()
						return Response(status=status.HTTP_200_OK)
						# raise serializers.ValidationError("Failed to Create: Can't duplicate Cart Item, try changing quantity.")

		serializer = self.get_serializer(data=f_d)
		serializer.is_valid(raise_exception=True)

		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		
		## Can only update quantity
		if int(instance.product.id) != int(request.data["product"]):
			raise serializers.ValidationError("Failed to Update: Can't modify this field, try changing quantity.")
		
		if int(instance.order.id) != int(request.data["order"]):
			raise serializers.ValidationError("Failed to Update: Can't modify this field. ")

		if int(request.data["quantity"]) == 0:
			self.destroy(self, request)
			return Response(status=status.HTTP_204_NO_CONTENT) 
		
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
		    # If 'prefetch_related' has been applied to a queryset, we need to
		    # forcibly invalidate the prefetch cache on the instance.
		    instance._prefetched_objects_cache = {}

		return Response(serializer.data)




class OrderModelViewSet(ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, DeleteNotAllowed]
	authentication_classes = (TokenAuthentication,)
	
	def get_queryset(self):
		return self.queryset.filter(account=self.request.user.account).order_by('-created')

	@action(methods=['GET'], detail=True, url_name='final payment')
	def final_payment(self, request,*args, **kwargs):
		instance = self.get_object()
		payments = instance.payments.all()
		if len(payments) == 0:
			return serializers.ValidationError("First payment not made yet.")
		elif len(payments) == 1:
			if payments[0].status == 'success':
				amount_due = instance.final_payment_amount()
				order_val_for_stripe = int(round((amount_due * 100), 2))
				# intent = stripe.PaymentIntent.create(amount=order_val_for_stripe,currency="inr",)	
				# Payment.objects.create(order=instance,amount=amount_due,status='checkout',
				# 					   intent_secret=intent.client_secret,intent_key=intent.id)

				# in prod delete line below and uncomment both above
				Payment.objects.create(order=instance,amount=amount_due,status='checkout',  
									   intent_secret='',intent_key='') 
			else:
				raise serializers.ValidationError('First payment not complete.')
		partial = kwargs.pop('partial', False)
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
		    # If 'prefetch_related' has been applied to a queryset, we need to
		    # forcibly invalidate the prefetch cache on the instance.
		    instance._prefetched_objects_cache = {}

		return Response(serializer.data)

	def delete(self,request, *args, **kwargs):
		return Response({"Not allowed."}, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, *args, **kwargs):
		
		instance = self.get_object()
		instance_payments = instance.payments.all()
		intent_key = instance.payments.all()[0].intent_key
		payment_id = instance.payments.all()[0].id
		

		# if bool(request.data.get("mounted")) == False and instance.status != 'success':
		# 	raise serializers.ValidationError("Invalid state flow: Can't use this value.")
		
		if request.data["status"] == "gold_paid": 
			# stripe_intent = stripe.PaymentIntent.retrieve(intent_key)
			intent_status = 'succeeded' # temp variable switch with stripe_intent.status
			if instance.status != 'checkout':
				raise serializers.ValidationError("Invalid state flow: Can't use this value.")

			if len(instance_payments) == 1:
		
				if intent_status != 'succeeded':
					raise serializers.ValidationError("Payment not processed/successful.")
				elif intent_status == 'succeeded':
					payment = Payment.objects.get(id=payment_id)
					payment.status = 'success'
					payment.intent_secret = ''
					payment.save()
			else:
				raise serializers.ValidationError("Invalid state flow: Can't use this value.")

		
		if request.data["status"] == 'success':
			if instance.status != 'gold_paid':
				raise serializers.ValidationError("Invalid state flow: Can't use this value.")

			if len(instance_payments) == 2:
				intent_key = instance_payments[1].intent_key
				# stripe_intent = stripe.PaymentIntent.retrieve(intent_key)
				stripe_intent_status = 'succeeded'
				if stripe_intent_status != 'succeeded': # replace variable w stripe_intent.status and uncomment above ^
					raise serializers.ValidationError("Forbidden Action: Payment not processed/successful.")
				elif stripe_intent_status == 'succeeded' :
					for payment in instance.payments.all():
						if payment.status == 'checkout':
							p = Payment.objects.get(id=payment.id)
							p.status = 'success'
							p.intent_secret= ''
							p.save()
							instance.status = 'success'
							# instance.mounted = False
			else:
				raise serializers.ValidationError("Order doesn't have valid params to be considered a success.")

			if request.data["status"] == 'checkout':
				serializers.ValidationError("Invalid state flow: Can't use this value.")


		partial = kwargs.pop('partial', False)
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
		    # If 'prefetch_related' has been applied to a queryset, we need to
		    # forcibly invalidate the prefetch cache on the instance.
		    instance._prefetched_objects_cache = {}

		return Response(serializer.data)
	
	
class CheckoutListAPIView(ListAPIView):

	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated ]
	authentication_classes = (TokenAuthentication,)

	def get_queryset(self):
		return self.queryset.filter(account=self.request.user.account, status='checkout')

	def list(self,request, *args, **kwargs):

		if self.request.user.is_anonymous:
			return Response({
				"Error": "Sign in Required to perform action."
				},status=status.HTTP_400_BAD_REQUEST,)

		queryset = self.filter_queryset(self.get_queryset())

	
		if len(queryset) == 0:
			return Response({
				"Error": "Cart is empty."
				},status=status.HTTP_400_BAD_REQUEST,)

		if len(queryset) == 1:
			for order in queryset:
				if order.order_value() == 0:
					return Response({
				"Error": "Cart is empty."
				},status=status.HTTP_400_BAD_REQUEST,)

				for li in order.line_items.all():
					prod_targ = Product.objects.get(id=int(li.product.id))
					li_quant = int(li.quantity)
					prod_quant = prod_targ.quantity
					
					if int(prod_targ.quantity) == 0:
						raise serializers.ValidationError(f"{prod_targ.title} not in stock. Please delete from cart.")
					elif int(prod_quant) < int(li_quant):
						raise serializers.ValidationError(f"{prod_targ.title} :{prod_quant} item(s) left in stock. Adjust quantity.")
		

				payment_amount = order.first_payment_amount()
				order_val_for_stripe = int(round((payment_amount * 100), 2))
				all_payments = order.payments.all()

				if len(all_payments) == 0:
	
					# intent = stripe.PaymentIntent.create(amount=order_val_for_stripe,currency="inr",)	
					# new_payment_obj = Payment.objects.create(order=order,amount=payment_amount,status="checkout", 
					# 										 intent_secret=intent.client_secret, intent_key=intent.id)
					# payment_key = intent.id

					# uncomment above in production ^^ and delete two lines below

					new_payment_obj = Payment.objects.create(order=order,amount=payment_amount,status="checkout", 
															 intent_secret='', intent_key='')


				# uncomment during stripe integration 
				# if len(all_payments) == 1:
					# if  all_payments[0].intent_key != '':
						# payment_key = all_payments[0].intent_key
						# intent = stripe.PaymentIntent.retrieve(payment_key)
						# if order_val_for_stripe != intent.amount:
							# stripe.PaymentIntent.modify(sid=payment_key, amount=payment_amount)
					
		queryset = self.filter_queryset(self.get_queryset())
		
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		if float(serializer.data[0]["order_value"]) == 0.0:
			raise serializers.ValidationError("Add Item(s) to Cart.")
		

		res = {}
		res["amount"] = serializer.data[0]["first_payment_amount"]
		res["url"] = serializer.data[0]["url"]
		res["intent_secret"] = serializer.data[0]["payments"][0]["intent_secret"]


		return Response(res)




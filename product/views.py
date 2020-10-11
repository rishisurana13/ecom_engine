from product.serializers import ProductSerializer, ProductSummarySerializer
from rest_framework.viewsets import ModelViewSet
from permissions.permissions import IsAdminUserOrReadOnly
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.models import Product
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from product.pagination import HomeViewPagination, CategoryListingViewPagination



class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [IsAdminUserOrReadOnly]
	authentication_classes = (TokenAuthentication,)
	pagination_class = CategoryListingViewPagination
	filter_backends = [DjangoFilterBackend]
	filter_fields = ['product_type',]

	def get_serializer_class(self):
		summary_requests = ('list')
		
		if self.action in summary_requests:
			return ProductSummarySerializer
		else:
			return ProductSerializer

	@action(methods=['GET'], detail=False, url_name='home')
	def home(self, request,*args, **kwargs):
		self.pagination_class = HomeViewPagination

		queryset = self.filter_queryset(self.get_queryset())

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


	


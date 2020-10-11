from rest_framework.pagination import LimitOffsetPagination

class HomeViewPagination(LimitOffsetPagination):
	default_limit = 15

class CategoryListingViewPagination(LimitOffsetPagination):
	default_limit = 20
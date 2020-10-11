from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class IsAdminUserOrReadOnly(permissions.IsAdminUser):

	def has_permission(self,request,view):
		is_admin = super().has_permission(request,view)
		return request.method in permissions.SAFE_METHODS or is_admin

class AdminCanReadOnly(permissions.IsAdminUser):

	def has_permission(self,request,view):
		is_admin = super().has_permission(request,view)
		if is_admin:
			return request.method in permissions.SAFE_METHODS

	

class IsUserAndAdminCanReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		is_admin = permissions.IsAdminUser.has_permission(self, request, view)

		if is_admin:
			return request.method in permissions.SAFE_METHODS
    	
		return obj.user == request.user

class IsAccountAndAdminCanReadOnly(permissions.BasePermission):
				
	def has_object_permission(self, request, view, obj):
		is_admin = permissions.IsAdminUser.has_permission(self, request, view)
		if is_admin:
			return request.method in permissions.SAFE_METHODS
		
		return obj.account.user == request.user


class IsAccountAndAdminCanReadOnlyCart(permissions.BasePermission):
				
	def has_object_permission(self, request, view, obj):
		is_admin = permissions.IsAdminUser.has_permission(self, request, view)
		if is_admin:
			return request.method in permissions.SAFE_METHODS
		
		return obj.order.account.user == request.user

class DeleteNotAllowed(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		NOT_ALLOWED = ('destroy', 'delete')
		if request.method.lower() in NOT_ALLOWED:
			return False
		else:
			return True
		
		





        




	



		


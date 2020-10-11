from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
	path('sign-up/', views.CreateUserView.as_view(),name='create'),
	path('sign-in/',views.CreateTokenView.as_view(),name='token'),
	path('profile/', views.ManageUserView.as_view(), name='me'),
	path('change-password/', views.ChangePasswordView.as_view(), name='change-pw'), 
	path('sign-out/', views.Logout.as_view(), name='sign-out')
	
]

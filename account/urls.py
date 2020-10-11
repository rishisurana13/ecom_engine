from django.urls import include, path
from rest_framework.routers import DefaultRouter
from account.views import AccountListAPIView, AccountRetrieveUpdateDestroyAPIView
from django.urls import path

urlpatterns = [
    path("accounts/", AccountListAPIView.as_view(), name='account-list' ),
    path("me/", AccountRetrieveUpdateDestroyAPIView.as_view(), name='account-detail'),


]
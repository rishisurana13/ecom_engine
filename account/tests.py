
from user import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

ACCOUNT_DETAIL_URL = reverse('account-detail')

class PublicAccountApiTests(TestCase):
	"""Test publicly available ingredients API"""

	def setUp(self):
		self.client = APIClient()


	def test_login_required(self):
		"""login is required to access the endpoint"""
		

		res = self.client.get(ACCOUNT_DETAIL_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountApiTests(TestCase):
	"""Test ingredients can be retrived by authorized user"""
	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'test@test.com',
			'password')

		self.client.force_authenticate(self.user)
		

	def test_account_exists(self):
		""" Test account exists and id no == user id"""

		self.assertEqual(self.user.account.id,self.user.id)

	def test_access_all_endpoints(self):

		res_acc_detail = self.client.get(reverse('account-detail'))
		res_acc_orders = self.client.get(reverse('order-list'))
		# res_checkout = self.client.get(reverse('checkout-view'))
		self.assertEqual(res_acc_detail.status_code, status.HTTP_200_OK)
		self.assertEqual(res_acc_orders.status_code, status.HTTP_200_OK)
		# self.assertEqual(res_checkout.status_code, status.HTTP_200_OK)

	

















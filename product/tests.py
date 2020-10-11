from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

PRODUCTS_URL = reverse('product-list')


class PrivateUserProductApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'test1@test1.com',
			'password'
			)

		self.client.force_authenticate(self.user)

	def test_auth_required(self):
		"""Test that authentication is required"""
		payload = {"title":"some product", "price":"100.00","product_type":"electronic","quantity":"", "discount":"0.0"}
		res = self.client.post(PRODUCTS_URL, payload)
		self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)

class PrivateAdminProductApiTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.superuser = get_user_model().objects.create_superuser(
			'test1@test1.com',
			'password',
			)

		self.client.force_authenticate(self.superuser)

	def test_admin_can_post(self):
		"""Test that authentication is required"""
		payload = {"title":"some product", "price":"100.00","product_type":"electronic","quantity":"", "discount":"0.0"}
		res = self.client.post(PRODUCTS_URL, payload)
		self.assertEqual(res.status_code,status.HTTP_201_CREATED)





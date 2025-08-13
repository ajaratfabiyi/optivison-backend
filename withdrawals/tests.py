from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class WithdrawalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="wuser@example.com",
            username="wuser",
            password="pass123",
            referred_by=None
        )
        self.user.referred_by = self.user
        self.user.save()
        self.client.login(email="wuser@example.com", password="pass123")

    def test_create_withdrawal(self):
        url = reverse("withdrawal-list")
        data = {
            "amount": "50.00",
            "bank_name": "Test Bank",
            "account_number": "1234567890",
            "account_name": "Test User"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_withdrawals(self):
        url = reverse("withdrawal-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

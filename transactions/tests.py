from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from transactions.models import Transaction

class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="tuser@example.com",
            username="tuser",
            password="pass123",
            referred_by=None
        )
        self.user.referred_by = self.user
        self.user.save()
        self.client.login(email="tuser@example.com", password="pass123")

    def test_create_transaction(self):
        url = reverse("transaction-list")
        data = {
            "tx_type": "deposit",
            "amount": "100.00",
            "reference": "TX123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_transactions(self):
        Transaction.objects.create(user=self.user, tx_type="deposit", amount=100, reference="TXREF")
        url = reverse("transaction-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

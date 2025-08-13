from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class DashboardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="duser@example.com",
            username="duser",
            password="pass123",
            referred_by=None
        )
        self.user.referred_by = self.user
        self.user.save()
        self.client.login(email="duser@example.com", password="pass123")

    def test_user_stats(self):
        url = reverse("user-stats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

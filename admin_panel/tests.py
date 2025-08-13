from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class AdminPanelTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass"
        )
        self.client.login(email="admin@example.com", password="adminpass")

    def test_list_users(self):
        url = reverse("admin-users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

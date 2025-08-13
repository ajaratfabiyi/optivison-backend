from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass"
        )
        self.referrer = User.objects.create_user(
            email="referrer@example.com",
            username="referrer",
            password="refpass",
            referred_by=None
        )
        self.referrer.referred_by = self.referrer  # self-ref to bypass validation in setup
        self.referrer.save()

    def test_user_registration_with_referral(self):
        url = reverse("register")
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "testpass123",
            "referral_code": self.referrer.referral_code
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse("token_obtain_pair")
        data = {"email": "referrer@example.com", "password": "refpass"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_access_requires_auth(self):
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

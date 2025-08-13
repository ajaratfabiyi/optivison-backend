from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from kyc.models import KYCSubmission
from django.core.files.uploadedfile import SimpleUploadedFile

class KYCTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            username="user1",
            password="pass123",
            referred_by=None
        )
        self.user.referred_by = self.user
        self.user.save()
        self.client.login(email="user@example.com", password="pass123")

    def test_submit_kyc(self):
        url = reverse("submit_kyc")
        file = SimpleUploadedFile("doc.png", b"fakecontent", content_type="image/png")
        data = {"document_type": "passport", "document_file": file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_kyc_status(self):
        KYCSubmission.objects.create(user=self.user, document_type="passport", document_file="test.png")
        url = reverse("kyc_status")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json
import stripe

class WebhookTests(APITestCase):
    def test_stripe_webhook_invalid_signature(self):
        url = reverse("stripe-webhook")
        payload = json.dumps({"id": "evt_test", "type": "payment_intent.succeeded"})
        response = self.client.post(url, data=payload, content_type="application/json", HTTP_STRIPE_SIGNATURE="invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

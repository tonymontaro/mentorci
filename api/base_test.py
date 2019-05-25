import json
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient


class BaseViewTest(APITestCase):
    """Base Test Class"""

    client = APIClient()
    test_email = "test@mail.com"
    test_password = "testing"

    def login_a_user(self, email="", password=""):
        """Login a user for testing."""
        url = reverse("auth-login", kwargs={"version": "v1"})
        return self.client.post(
            url,
            data=json.dumps({"email": email, "password": password}),
            content_type="application/json"
        )

    def login_client(self):
        """Login a user and authenticate the client."""
        url = reverse("auth-login", kwargs={"version": "v1"})
        response = self.client.post(
            url,
            data=json.dumps(
                {"email": self.test_email, "password": self.test_password}),
            content_type="application/json"
        )
        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(email=self.test_email, password=self.test_password)
        return self.token

    def register_a_user(self, email="", password=""):
        """Register a user for testing."""
        return self.client.post(
            reverse("auth-register", kwargs={"version": "v1"}),
            data=json.dumps({"email": email, "password": password, }),
            content_type='application/json'
        )

    def setUp(self):
        """Create admin user for testing."""
        self.user = User.objects.create_superuser(
            username=self.test_email,
            email=self.test_email,
            password=self.test_password
        )

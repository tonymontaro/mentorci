import json
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status


class BaseViewTest(APITestCase):
    client = APIClient()

    def login_a_user(self, email="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, email="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    'email': email,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(email=email, password=password)
        return self.token

    def register_a_user(self, email="", password=""):
        return self.client.post(
            reverse(
                "auth-register",
                kwargs={
                    "version": "v1"
                }
            ),
            data=json.dumps(
                {
                    "email": email,
                    "password": password,
                }
            ),
            content_type='application/json'
        )

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test@mail.com",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )


# Create your tests here.
class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test@mail.com", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """

    def test_register_a_user(self):
        response = self.register_a_user(email="new_user@mail.com",
                                        password="new_user_pass")
        # assert status code is 201 CREATED
        self.assertEqual(response.data["email"], "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_a_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

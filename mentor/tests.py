from rest_framework.views import status
from django.urls import reverse

from api.base_test import BaseViewTest


class LoginMentorTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user(self):
        response = self.login_a_user("test@mail.com", "testing")
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.login_a_user("anonymous", "pass")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterMentorTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """

    def test_register_a_user(self):
        response = self.register_a_user(email="new_user@mail.com",
                                        password="new_user_pass")
        self.assertEqual(response.data["email"], "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.register_a_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateMentorTest(BaseViewTest):
    """
    Tests for mentors/:id endpoint
    """

    def test_update_a_user(self):
        self.login_client()

        fullname = 'Uchiya Montaro'
        response = self.client.put(
            reverse("update-mentor", kwargs={"version": "v1", "pk": 1}),
            data={'fullname': fullname}
        )
        self.assertEqual(response.data["email"], "test@mail.com")
        self.assertEqual(response.data["fullname"], fullname)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

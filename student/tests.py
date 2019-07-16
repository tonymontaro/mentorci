from rest_framework.views import status
from django.urls import reverse

from api.base_test import BaseViewTest
from .models import STAGES


class BaseStudentTest(BaseViewTest):
    """Base Student Test Class"""

    student = {'name': 'Uzi Nakamura', 'email': 'uzi-naks@m.com',
               'stage': '', 'github': ''}

    def create_student(self):
        self.login_client()
        return self.client.post(reverse(
            "student-list-create", kwargs={"version": "v1"}),
            data=self.student)

    def get_students(self):
        self.login_client()
        return self.client.get(
            reverse("student-list-create", kwargs={"version": "v1"}))


class ListCreateStudentTest(BaseStudentTest):
    """
    Tests for the students/ endpoint
    """

    def test_create_student(self):
        response = self.create_student()
        self.assertEqual(response.data['email'], self.student['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_students(self):
        response = self.get_students()
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.create_student()
        response = self.get_students()
        self.assertEqual(len(response.data), 1)


class StudentDetailTest(BaseStudentTest):
    """
    Tests for the students/:id/ endpoint
    """

    def test_get_student(self):
        self.create_student()

        response = self.client.get(reverse(
            "student-detail", kwargs={"version": "v1", 'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_student(self):
        self.login_client()

        response = self.client.get(reverse(
            "student-detail", kwargs={"version": "v1", 'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_student(self):
        self.create_student()

        updated_detail = {'email': 'uzi-nakamura@gm.com'}
        response = self.client.put(reverse(
            "student-detail", kwargs={"version": "v1", 'pk': 1}),
            data=updated_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], updated_detail['email'])


class GetStagesTest(BaseViewTest):
    """
    Tests Getting Stages
    """

    def test_get_stages(self):
        self.login_client()

        response = self.client.get(reverse(
            "options", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['stages'], STAGES)

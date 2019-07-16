from rest_framework.views import status
from django.urls import reverse

from api.base_test import BaseViewTest


class BaseFeedbackTest(BaseViewTest):
    """Base Feedback Test Class"""

    def setUp(self):
        super().setUp()

        self.login_client()
        self.student = self.client.post(reverse(
            "student-list-create", kwargs={"version": "v1"}),
            data={'name': 'Uzi Nakamura', 'email': 'uzi-naks@m.com',
                  'stage': '', 'github': ''}).data
        self.feedback = {
            'student': self.student['id'],
            'score': 65,
            'summary': 'intro',
            'project': 'other'
        }

    def create_feedback(self, data=None):
        data = data or self.feedback
        return self.client.post(reverse(
            "feedback-list-create", kwargs={"version": "v1"}),
            data=data)

    def get_feedback(self):
        return self.client.get(
            reverse("feedback-list-create", kwargs={"version": "v1"}))


class ListCreateFeedbackTest(BaseFeedbackTest):
    """
    Tests for the feedback/ endpoint
    """

    def test_create_feedback(self):
        response = self.create_feedback()
        self.assertEqual(response.data['summary'], self.feedback['summary'])
        self.assertEqual(response.data['score'], self.feedback['score'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_feedback(self):
        feedback = dict(self.feedback)
        feedback['student'] = 'asdf'
        response = self.create_feedback(feedback)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_feedback(self):
        response = self.get_feedback()
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.create_feedback()
        response = self.get_feedback()
        self.assertEqual(len(response.data), 1)

    def test_get_student_feedback(self):
        self.create_feedback()
        response = self.client.get(reverse(
            "student-feedback",
            kwargs={"version": "v1", 'student_id': self.student['id']}))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FeedbackDetailTest(BaseFeedbackTest):
    """
    Tests for the feedback/:id/ endpoint
    """

    def test_delete_feedback(self):
        feedback = self.create_feedback().data

        response = self.client.delete(reverse(
            "feedback-detail",
            kwargs={"version": "v1", 'pk': feedback['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

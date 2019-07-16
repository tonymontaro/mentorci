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

    def get_feedbacks(self):
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

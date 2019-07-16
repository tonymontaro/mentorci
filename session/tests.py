from rest_framework.views import status
from django.urls import reverse

from api.base_test import BaseViewTest
from .models import SESSION_TYPES, SESSION_FEELINGS


class BaseSessionTest(BaseViewTest):
    """Base Session Test Class"""

    def setUp(self):
        super().setUp()

        self.login_client()
        self.student = self.client.post(reverse(
            "student-list-create", kwargs={"version": "v1"}),
            data={'name': 'Uzi Nakamura', 'email': 'uzi-naks@m.com',
                  'stage': '', 'github': ''}).data
        self.session = {
            'student': self.student['id'],
            'summary': 'intro',
            'date': '2019-05-25',
            'types': 'other',
            'projects': '["other"]',
            'duration': '01-20-30',
            'feeling': 'average'
        }

    def create_session(self, data=None):
        data = data or self.session
        return self.client.post(reverse(
            "session-list-create", kwargs={"version": "v1"}),
            data=data)

    def get_sessions(self):
        return self.client.get(
            reverse("session-list-create", kwargs={"version": "v1"}))


class ListCreateSessionTest(BaseSessionTest):
    """
    Tests for the sessions/ endpoint
    """

    def test_create_sessions(self):
        response = self.create_session()
        self.assertEqual(response.data['summary'], self.session['summary'])
        self.assertEqual(response.data['durationInMins'], '80.5')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_sessions(self):
        session = dict(self.session)
        session['date'] = 'wrong-date'
        response = self.create_session(session)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_sessions(self):
        response = self.get_sessions()
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.create_session()
        response = self.get_sessions()
        self.assertEqual(len(response.data), 1)


class SessionDetailTest(BaseSessionTest):
    """
    Tests for the sessions/:id/ endpoint
    """

    def test_get_session(self):
        self.create_session()

        response = self.client.get(reverse(
            "session-detail", kwargs={"version": "v1", 'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_session(self):
        self.login_client()

        response = self.client.get(reverse(
            "session-detail", kwargs={"version": "v1", 'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_session(self):
        self.create_session()

        updated_detail = {'summary': 'code review.'}
        response = self.client.put(reverse(
            "session-detail", kwargs={"version": "v1", 'pk': 1}),
            data=updated_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], updated_detail['summary'])

    def test_delete_session(self):
        session = self.create_session().data

        response = self.client.delete(reverse(
            "session-detail",
            kwargs={"version": "v1", 'pk': session['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetSessionTypesTest(BaseViewTest):
    """
    Tests for Session Types option
    """

    def test_get_session_types(self):
        self.login_client()

        response = self.client.get(reverse(
            "options", kwargs={"version": "v1"}))
        expected = [list(item) for item in SESSION_TYPES]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['types'], expected)


class GetSessionFellingsTest(BaseViewTest):
    """
    Tests for the sessions/stages/ endpoint
    """

    def test_get_session_feelings(self):
        self.login_client()

        response = self.client.get(reverse(
            "options", kwargs={"version": "v1"}))
        expected = [list(item) for item in SESSION_FEELINGS]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['feelings'], expected)

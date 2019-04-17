import os

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.http import JsonResponse

from .models import SessionLog, SESSION_TYPES, SESSION_FEELINGS
from .serializers import SessionLogSerializer, DetailedSessionLogSerializer
from student.models import Student
from .decorators import validate_session_create_data

SESSION_TYPES_DICT = dict(SESSION_TYPES)
SESSION_FEELINGS_DICT = dict(SESSION_FEELINGS)


class ListCreateSessionLogView(generics.ListCreateAPIView):
    """
    GET students/
    POST students/
    """
    serializer_class = SessionLogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return SessionLog.objects.filter(mentor=self.request.user)

    @staticmethod
    def _fill_google_form(id):
        if os.getenv('E2E', 'false') == 'true':
            os.system(
                'LOGID={} ./node_modules/.bin/nightwatch'.format(id))

    @validate_session_create_data
    def post(self, request, *args, **kwargs):
        try:
            student = Student.objects.filter(mentor=self.request.user).get(
                pk=request.data.get('student'))
            session = SessionLog.objects.create(
                student=student,
                summary=request.data.get('summary'),
                concern=request.data.get('concern'),
                date=request.data.get('date'),
                types=request.data.get('types'),
                duration=request.data.get('duration'),
                feeling=request.data.get('feeling'),
                mentor=request.user
            )
            return Response(
                data=SessionLogSerializer(session).data,
                status=status.HTTP_201_CREATED
            )
        except Student.DoesNotExist:
            return Response(
                data={
                    "message": "None of your students has an ID of {}".format(
                        request.data.get('student'))},
                status=status.HTTP_404_NOT_FOUND
            )


class SessionLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET students/:id/
    PUT students/:id/
    DELETE students/:id/
    """
    queryset = SessionLog.objects.all()
    serializer_class = SessionLogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def _session_not_found(self, pk):
        return Response(
            data={
                "message": "None of your sessions has an ID of {}".format(pk)},
            status=status.HTTP_404_NOT_FOUND
        )

    def get(self, request, *args, **kwargs):
        try:
            session = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            if request.GET.get('detailed', '').lower() == 'true':
                session.types = '|'.join(
                    [SESSION_TYPES_DICT.get(t, '') for t in
                     session.types.split('|')])
                session.feeling = SESSION_FEELINGS_DICT.get(session.feeling, '')
                return Response(DetailedSessionLogSerializer(session).data)
            return Response(SessionLogSerializer(session).data)
        except SessionLog.DoesNotExist:
            return self._session_not_found(kwargs['pk'])

    @validate_session_create_data
    def put(self, request, *args, **kwargs):
        try:
            session = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            serializer = SessionLogSerializer()
            updated_session = serializer.update(session, request.data)
            return Response(SessionLogSerializer(updated_session).data)
        except SessionLog.DoesNotExist:
            return self._session_not_found(kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        try:
            session = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            session.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SessionLog.DoesNotExist:
            return self._session_not_found(kwargs['pk'])


def session_types(request, version):
    return JsonResponse(SESSION_TYPES, safe=False)


def session_feelings(request, version):
    return JsonResponse(SESSION_FEELINGS, safe=False)

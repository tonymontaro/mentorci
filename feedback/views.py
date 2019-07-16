from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.http import JsonResponse

from .models import Feedback
from .serializers import FeedbackSerializer
from student.models import Student


class ListCreateFeedbackView(generics.ListCreateAPIView):
    """
    GET feedback/
    POST students/
    """
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Feedback.objects.filter(mentor=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            student = Student.objects.filter(mentor=self.request.user).get(
                pk=request.data.get('student'))
            feedback = Feedback.objects.create(
                student=student,
                mentor=request.user,
                summary=request.data.get('summary'),
                score=int(request.data.get('score')),
                project=request.data.get('project'),
            )
            return Response(
                data=FeedbackSerializer(feedback).data,
                status=status.HTTP_201_CREATED
            )
        except Student.DoesNotExist:
            return Response(
                data={
                    "message": "None of your students has an ID of {}".format(
                        request.data.get('student'))},
                status=status.HTTP_404_NOT_FOUND
            )


class FeedbackDetailView:
    pass

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
        studentID = request.data.get('student')
        try:
            score = request.data.get('score')
            if not str(score).isnumeric() or not str(studentID).isnumeric():
                return Response(
                    data={
                        "message": 'student and score should be numeric.'},
                    status=status.HTTP_400_BAD_REQUEST)
            student = Student.objects.filter(mentor=self.request.user).get(
                pk=studentID)
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
                        studentID)},
                status=status.HTTP_404_NOT_FOUND
            )


class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DELETE feedback/:id/
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        try:
            feedback = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            feedback.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Feedback.DoesNotExist:
            return Response(
                data={
                    "message": "Feedback with ID {} not found.".format(
                        kwargs['pk'])},
                status=status.HTTP_404_NOT_FOUND
            )


def get_student_feedback(request, version, *args, **kwargs):
    feedback = Feedback.objects.filter(student=kwargs['student_id'])
    return JsonResponse(
        FeedbackSerializer(feedback, many=True).data, safe=False)
# d

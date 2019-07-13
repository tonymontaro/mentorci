from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.http import JsonResponse

from .models import Student, STAGES
from .serializers import StudentSerializer
from .decorators import validate_student_create_data


class ListCreateStudentView(generics.ListCreateAPIView):
    """
    GET students/
    POST students/
    """
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Student.objects.filter(mentor=self.request.user).order_by('name')

    @validate_student_create_data
    def post(self, request, *args, **kwargs):
        student = Student.objects.create(
            name=request.data.get('name'),
            email=request.data.get('email'),
            stage=request.data.get('stage'),
            github=request.data.get('github'),
            mentor=request.user
        )
        return Response(
            data=StudentSerializer(student).data,
            status=status.HTTP_201_CREATED
        )


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET students/:id/
    PUT students/:id/
    DELETE students/:id/
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def _student_not_found(self, pk):
        return Response(
            data={
                "message": "None of your students has an ID of {}".format(pk)},
            status=status.HTTP_404_NOT_FOUND
        )

    def get(self, request, *args, **kwargs):
        try:
            student = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            return Response(StudentSerializer(student).data)
        except Student.DoesNotExist:
            return self._student_not_found(kwargs['pk'])

    def put(self, request, *args, **kwargs):
        try:
            student = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            serializer = StudentSerializer()
            updated_student = serializer.update(student, request.data)
            return Response(StudentSerializer(updated_student).data)
        except Student.DoesNotExist:
            return self._student_not_found(kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        try:
            student = self.queryset.filter(mentor=self.request.user).get(
                pk=kwargs["pk"])
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return self._student_not_found(kwargs['pk'])


def student_stages(request, version):
    return JsonResponse(STAGES, safe=False)

# Todo; Handle DataBase failure

from django.urls import path
from .views import ListCreateStudentView, StudentDetailView, student_stages

urlpatterns = [
    path('students/', ListCreateStudentView.as_view(),
         name="student-list-create"),
    path('students/<int:pk>/', StudentDetailView.as_view(),
         name="student-detail"),
    path('students/stages/', student_stages, name="student-stages")
]

from django.urls import path
from .views import ListCreateStudentView, StudentDetailView

urlpatterns = [
    path('students/', ListCreateStudentView.as_view(),
         name="student-list-create"),
    path('students/<int:pk>/', StudentDetailView.as_view(),
         name="student-detail"),
]

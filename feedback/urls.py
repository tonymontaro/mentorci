from django.urls import path
from .views import ListCreateFeedbackView, FeedbackDetailView, \
    get_student_feedback

urlpatterns = [
    path('feedback/', ListCreateFeedbackView.as_view(),
         name="feedback-list-create"),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(),
         name="feedback-detail"),
    path('student/<int:student_id>/feedback/', get_student_feedback,
         name="student-feedback"),
]

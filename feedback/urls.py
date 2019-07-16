from django.urls import path
from .views import ListCreateFeedbackView, FeedbackDetailView

urlpatterns = [
    path('feedback/', ListCreateFeedbackView.as_view(),
         name="feedback-list-create")
]

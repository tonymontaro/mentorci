from django.urls import path
from .views import ListCreateSessionLogView, SessionLogDetailView

urlpatterns = [
    path('sessions/', ListCreateSessionLogView.as_view(),
         name="session-list-create"),
    path('sessions/<int:pk>/', SessionLogDetailView.as_view(),
         name="session-detail"),
]

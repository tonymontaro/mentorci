from django.urls import path
from .views import LoginView, RegisterUsers, UpdateMentor


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('mentors/<int:pk>/', UpdateMentor.as_view(), name="update-mentor")
]

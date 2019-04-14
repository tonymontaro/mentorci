from django.urls import path
from .views import LoginView, RegisterUsers


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]

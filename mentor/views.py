from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def login_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user.token = jwt_encode_handler(
            jwt_payload_handler(user)
        )
        serializer = UserSerializer(user)
        return serializer.data
    return False


class LoginView(generics.RetrieveAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("email", "")
        password = request.data.get("password", "")
        user_data = login_user(request, username, password)
        if user_data:
            return Response(user_data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        fullname = request.data.get("fullname", "")
        bio = request.data.get("bio", "")
        username = email
        if not username and not password and not email:
            return Response(
                data={
                    "message": "email and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        new_user.profile.fullname = fullname
        new_user.profile.bio = bio
        new_user.profile.save()
        user_data = login_user(request, username, password)

        return Response(
            data=user_data,
            status=status.HTTP_201_CREATED
        )

class UpdateMentor(generics.UpdateAPIView):
    """
    POST mentors/:id
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            mentor = self.queryset.get(pk=kwargs["pk"])
            serializer = UserSerializer()
            updated_mentor = serializer.update(mentor, request.data)
            updated_mentor.token = jwt_encode_handler(
                jwt_payload_handler(updated_mentor)
            )
            return Response(UserSerializer(updated_mentor).data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "Mentor with ID {} not found.".format(kwargs["pk"])},
                status=status.HTTP_404_NOT_FOUND
            )

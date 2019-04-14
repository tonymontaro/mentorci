from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True, source="profile.fullname")
    bio = serializers.CharField(read_only=True, source="profile.bio")
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ("id", "email", "fullname", "bio", "token")

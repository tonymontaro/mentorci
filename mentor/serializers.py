from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True, source="profile.fullname")
    bio = serializers.CharField(source="profile.bio")
    token = serializers.CharField(max_length=255)
    address = serializers.CharField(source="profile.address")
    address_more = serializers.CharField(source="profile.address_more")
    city_country = serializers.CharField(source="profile.city_country")

    class Meta:
        model = User
        fields = ("id", "email", "fullname", "bio", "token", "address", "address_more", "city_country")

    def update(self, instance, validated_data):
        instance.profile.fullname = validated_data.get("fullname", instance.profile.fullname)
        instance.profile.bio = validated_data.get("bio", instance.profile.bio)
        instance.profile.address = validated_data.get("address", instance.profile.address)
        instance.profile.address_more = validated_data.get("address_more", instance.profile.address_more)
        instance.profile.city_country = validated_data.get("city_country", instance.profile.city_country)
        instance.profile.save()
        return instance

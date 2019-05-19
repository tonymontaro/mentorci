from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    mentorID = serializers.CharField(read_only=True, source="mentor.id")

    class Meta:
        model = Student
        fields = ("id", "name", "email", "stage", "github", "mentorID", "about")

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.stage = validated_data.get("stage", instance.stage)
        instance.github = validated_data.get("github", instance.github)
        instance.about = validated_data.get("about", instance.about)
        instance.save()
        return instance

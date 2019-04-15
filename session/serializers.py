from rest_framework import serializers

from .models import SessionLog


class SessionLogSerializer(serializers.ModelSerializer):
    durationInMins = serializers.CharField(
        read_only=True, source="duration_in_mins")

    class Meta:
        model = SessionLog
        fields = (
            "id", "student", "mentor", "summary", "concern", "date",
            "types", "duration", "durationInMins", "feeling")

    def update(self, instance, validated_data):
        instance.summary = validated_data.get("summary", instance.summary)
        instance.concern = validated_data.get("concern", instance.concern)
        instance.date = validated_data.get("date", instance.date)
        instance.types = validated_data.get("types", instance.types)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.feeling = validated_data.get("feeling", instance.feeling)
        instance.save()
        return instance


class DetailedSessionLogSerializer(serializers.ModelSerializer):
    durationInMins = serializers.CharField(
        read_only=True, source="duration_in_mins")
    mentorEmail = serializers.CharField(read_only=True, source="mentor.email")
    studentEmail = serializers.CharField(read_only=True, source="student.email")
    mentorName = serializers.CharField(
        read_only=True, source="mentor.profile.fullname")

    class Meta:
        model = SessionLog
        fields = (
            "id", "student", "mentor", "summary", "concern", "date",
            "types", "duration", "durationInMins", "feeling", "mentorEmail",
            "studentEmail", "mentorName"
        )

from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("id", "student", "mentor", "summary", "project", "score")

    def update(self, instance, validated_data):
        instance.summary = validated_data.get("summary", instance.summary)
        instance.project = validated_data.get("project", instance.project)
        instance.score = validated_data.get("score", instance.score)
        instance.save()
        return instance

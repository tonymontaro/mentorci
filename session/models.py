import re

from django.db import models
from django.contrib.auth.models import User

from student.models import Student


class SessionLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=500, default="")
    concern = models.TextField(max_length=500, default="")
    date = models.CharField(max_length=255, blank=False)
    types = models.CharField(max_length=255, blank=False)
    duration = models.CharField(
        max_length=255, blank=False)
    feeling = models.TextField(blank=False)

    @property
    def duration_in_mins(self):
        hours, mins, seconds = map(int, self.duration.split('-'))
        return round(hours * 60 + mins + seconds / 60, 2)

    def __str__(self):
        return "Log: {} -> {}".format(self.id, self.date)

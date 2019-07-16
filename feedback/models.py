from django.db import models
from django.contrib.auth.models import User

from student.models import Student
from session.models import PROJECTS


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.CharField(max_length=255, blank=False, choices=PROJECTS)
    score = models.IntegerField(null=False)
    summary = models.TextField(max_length=500, default="")

    def __str__(self):
        return "Feedback: {} -> {}".format(self.id, self.student.name)

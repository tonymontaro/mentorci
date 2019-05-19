from django.db import models
from django.contrib.auth.models import User

STAGES = [
    "User Centric Frontend Development",
    "Interactive Frontend Development",
    "Practical Python",
    "Data Centric Development",
    "Full Stack Frameworks with Django"
]


class Student(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, unique=True, blank=False)
    stage = models.CharField(max_length=255, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    github = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return "Student; {}".format(self.name)

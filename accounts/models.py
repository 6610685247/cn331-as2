from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentid = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return f"{self.user.username} ({self.studentid})"
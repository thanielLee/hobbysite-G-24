from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    name = models.CharField(max_length=63)
    email = models.EmailField()

    def __str__(self):
        return self.name

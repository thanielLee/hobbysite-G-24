from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    display_name = models.CharField(max_length=63)
    email = models.EmailField(blank=True, unique=True)

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('profile:update', args=[str(self.pk)])
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_user_profile, sender=User)

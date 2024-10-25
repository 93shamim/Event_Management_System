# registration/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings  # Import settings

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated

    def __str__(self):
        return self.user.username
    


# signals.py
@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # Updated
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # Updated
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

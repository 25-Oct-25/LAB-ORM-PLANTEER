# accounts/models.py

from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return f'users/user_{instance.user.id}/profile_pics/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    about = models.TextField(blank=True) 
    avatar = models.ImageField(
        upload_to="images/avatars/", 
        default='images/avatars/avatar.webp', 
        blank=True
    )
    website_link = models.URLField(blank=True)
    
    def __str__(self):
        return f"Profile {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
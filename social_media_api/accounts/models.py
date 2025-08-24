from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

def profile_upload_path(instance, filename):
    return f'profiles/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_upload_path, blank=True, null=True)
    # users this user is following (their "following" list)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)

    def __str__(self):
        return self.username

    def follow(self, user):
        """Follow another user."""
        if user != self:  # Prevent following yourself
            self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user."""
        self.following.remove(user)    
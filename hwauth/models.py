from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DiscordID(models.Model):
    """
    Used in a one-to-one relationship with Django's default user class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discord_id = models.BigIntegerField()
    avatar = models.URLField()

    def __str__(self):
        return self.user.username

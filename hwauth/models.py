import requests
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models


# Create your models here.


class DiscordID(models.Model):
    """
    Used in a one-to-one relationship with Django's default user class
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discord_id = models.BigIntegerField()
    avatar_link = models.URLField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            response = requests.get(self.avatar_link)
            filename = self.avatar_link.rsplit('/', 1)[1] + ".png"

            self.avatar = SimpleUploadedFile(filename, response.content, content_type=response.headers['content-type'])
        finally:
            super(DiscordID, self).save()

from django.db import models
from django.contrib.auth.models import User

import os

# Create your models here.
from django.utils.text import slugify


class Event(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    event_date = models.DateTimeField()
    posted_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    participants = models.ManyToManyField(User, through='Participant', related_name='participant')
    slug = models.SlugField(max_length=50)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Event, self).save()

    def __str__(self):
        return self.title


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.__str__() + " is going to " + self.event.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_participant')
        ]


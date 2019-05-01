from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    event_date = models.DateTimeField()
    posted_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    participants = models.ManyToManyField(User, through='Participant', related_name='participant')

    def __str__(self):
        return self.title


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

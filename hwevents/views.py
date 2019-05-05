import datetime
import json
import sys

from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Count, Exists, OuterRef, F
from django.forms import ModelForm, DateTimeField
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from tempus_dominus.widgets import DateTimePicker

from hwauth.models import DiscordID
from hwevents.models import Event, Participant


# Create your views here.

def attend(request):
    event_id = request.POST.get('event')
    print(event_id, file=sys.stderr)

    user = request.user
    event = Event.objects.get(pk=event_id)

    if not Participant.objects.filter(user=user, event=event).exists():
        Participant.objects.create(user=user, event=event)
        return HttpResponse(201)
    else:
        return HttpResponse(500)


def cancel(request):
    event_id = request.POST.get('event')
    user = request.user
    event = Event.objects.get(pk=event_id)

    if Participant.objects.filter(user=user, event=event).exists():
        Participant.objects.get(user=user, event=event).delete()
        return HttpResponse(200)
    else:
        return HttpResponse(500)


def get_participants(request):
    """
    todo: Use DRF serializers to properly do this.
    user = User.objects.filter(user__in=participants).annotate(avatar=F('discordid__avatar'))
    cannot be properly serialized as base serializers only take into account the original model fields
    and not annotated (joined) fields
    """
    event_id = request.POST.get('event')

    participants = Participant.objects.filter(event=event_id)
    users = User.objects.filter(user__in=participants).annotate(avatar=F('discordid__avatar'))

    data = []
    for user in users:
        data.append({'username': user.username, 'avatar': user.avatar})

    return JsonResponse(data, safe=False)


class EventCreateForm(ModelForm):
    event_date = DateTimeField(
        widget=DateTimePicker
    )

    class Meta:
        model = Event
        fields = ['title', 'image', 'description', 'event_date']


def index(request):
    if request.method == "POST":
        form = EventCreateForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.writer = request.user
            event.save()

            return HttpResponseRedirect('/')
        else:
            return HttpResponse(form.errors)
    elif request.method == "GET":
        newest_events = Event.objects \
                            .filter(event_date__gt=datetime.datetime.now()) \
                            .annotate(going=Count('participants')) \
                            .order_by('event_date')[:10]

        if request.user.is_authenticated:
            user_events = Participant.objects.filter(user=request.user, event=OuterRef('pk'))
            newest_events = newest_events.annotate(user_going=Exists(user_events))

        create_form = EventCreateForm()

        return render(request, 'index.html', context={'newest_events': newest_events, 'form': create_form})

import datetime
import sys

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef, F
from django.forms import ModelForm, DateTimeField
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from tempus_dominus.widgets import DateTimePicker

from hwevents.models import Event, Participant


# Create your views here.

def attend(request):
    """
    API view called when the user presses the "Going" button.

    Creates a participant object using the currently authenticated user and the event id passed in.

    Returns an error if a participant somehow already exists.

    :param request: Request data
    :return: Http response denoting success or failure
    """
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
    """
    API view called when the user presses the "Cancel" button.

    Deletes a participant object using the currently authenticated user and the event id passed in.

    Returns an error if a participant doesn't exist to begin with

    :param request:
    :return:
    """
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
    Filters for participants by the passed in event id, and returns a list of users that are going to
    the event. Also includes discord IDs of those users.
    :param request: Request data
    :return: JSON containing an array of username + avatar objects
    """
    event_id = request.POST.get('event')

    participants = Participant.objects.filter(event=event_id)
    users = User.objects.filter(user__in=participants).annotate(avatar=F('discordid__avatar'))

    data = []
    for user in users:
        data.append({'username': user.username, 'avatar': user.avatar})

    return JsonResponse(data, safe=False)


class EventCreateForm(ModelForm):
    """
    Django form class that overrides the default Django date picker with
    Tempus Dominus' nicer bootstrap widget.
    """

    event_date = DateTimeField(
        widget=DateTimePicker
    )

    class Meta:
        model = Event
        fields = ['title', 'image', 'description', 'event_date']


def index(request):
    """
    TODO: separate form and index for clarity
    TODO: add scaling beyond 10 events either with fetching or tabulation

    Main event page that renders the main template for hwevents with the form and loads 10 newest templates as context

    If the user is authenticated, also adds to events' context if particular user is going

    Doubles as form submission handler on POST requests
    :param request: Request data
    :return: Rendered index page
    """
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

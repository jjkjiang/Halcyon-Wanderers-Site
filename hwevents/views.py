import datetime

import math
import sys

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef, F
from django.forms import ModelForm, DateTimeField, ModelChoiceField
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tempus_dominus.widgets import DateTimePicker

from hwevents.models import Event, Participant, Game, ParticipantRole, Role


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
    role = request.POST.get('role')

    user = request.user
    event = Event.objects.get(pk=event_id)

    if event.has_role:
        if role:
            participant = Participant.objects.create(user=user, event=event)
            roleobj = Role.objects.get(name=role)
            ParticipantRole.objects.create(participant=participant, role=roleobj)
        else:
            return HttpResponse(500)
    else:
        Participant.objects.create(user=user, event=event)

    return HttpResponse(201)


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

    Participant.objects.get(user=user, event=event).delete()
    return HttpResponse(200)


@csrf_exempt
def get_participants(request):
    """
    Filters for participants by the passed in event id, and returns a list of users that are going to
    the event. Also includes discord IDs of those users.

    If the event has roles, fetch role data as well
    :param request: Request data
    :return: JSON containing an array of username + avatar objects
    """
    event_id = request.POST.get('event')
    event = Event.objects.get(id=event_id)

    users = query_participants(event)

    data = []
    for user in users:
        dictionary = {'username': user.username,
                      'avatar': user.avatar,
                      'userid': user.userid}

        if event.has_role:
            role = Role.objects.get(participantrole__participant__user=user.id)

            dictionary['role'] = role.name
            dictionary['roleicon'] = role.icon.url

        data.append(dictionary)

    return JsonResponse(data, safe=False)


class EventCreateForm(ModelForm):
    """
    Django form class that overrides the default Django date picker with
    Tempus Dominus' nicer bootstrap widget.
    """

    event_date = DateTimeField(
        widget=DateTimePicker(
            options={
                "icons": {"time": "far fa-clock"}
            }
        )
    )

    class Meta:
        model = Event
        fields = ['title', 'image', 'description', 'event_date', 'has_role', 'game']


def index(request, page=1):
    """
    TODO: separate form and index for clarity
    TODO: add scaling beyond 10 events either with fetching or tabulation

    Main event page that renders the main template for hwevents with the form and current newest events

    If the user is authenticated, also adds to events' context if particular user is going

    Doubles as form submission handler on POST requests
    :param page: Page number of index
    :param request: Request data
    :return: Rendered index page
    """

    page = page - 1
    lower_page = 0 + (10 * page)
    upper_page = 10 + (10 * page)

    newest_events = Event.objects \
        .filter(event_date__gt=datetime.datetime.now()) \
        .annotate(going=Count('participants')) \
        .order_by('event_date')

    pages = math.ceil(newest_events.count() / 10)

    if request.user.is_authenticated:
        user_events = Participant.objects.filter(user=request.user, event=OuterRef('pk'))
        newest_events = newest_events.annotate(user_going=Exists(user_events))

    create_form = EventCreateForm()

    return render(request, 'index.html', context={'events': newest_events[lower_page:upper_page],
                                                  'form': create_form,
                                                  'pages': range(1, pages + 1),
                                                  'active_page': page + 1})


def create_event_view(request):
    if request.method == "POST":
        form = EventCreateForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.writer = request.user
            event.save()

            return HttpResponseRedirect('/')
        else:
            return HttpResponse(form.errors)


def all_events_view(request, page):
    if not page:
        return HttpResponseRedirect('/')
    page = page - 1

    lower_page = 0 + (10 * page)
    upper_page = 10 + (10 * page)

    page_events = Event.objects \
        .annotate(going=Count('participants')) \
        .order_by('event_date')

    if request.user.is_authenticated:
        user_events = Participant.objects.filter(user=request.user, event=OuterRef('pk'))
        page_events = page_events.annotate(user_going=Exists(user_events))

    pages = math.ceil(page_events.count() / 10)

    return render(request, 'index.html', context={'events': page_events[lower_page:upper_page],
                                                  'pages': range(1, pages + 1),
                                                  'active_page': page + 1})


def detail_view(request, slug, id):
    card = Event.objects \
        .annotate(going=Count('participants')) \
        .filter(slug=slug, id=id)

    if request.user.is_authenticated:
        user_events = Participant.objects.filter(user=request.user, event=OuterRef('pk'))
        card = card.annotate(user_going=Exists(user_events))

    return render(request, 'index.html', context={'events': card})


# Helper functions

def query_participants(event):
    """
    Obtains list of user objects with avatars and discord id annotated as fields
    :param event: event to query by
    :return: iterable queryset of user objects
    """
    participants = Participant.objects.filter(event=event)
    users = User.objects.filter(user__in=participants) \
        .annotate(avatar=F('discordid__avatar'),
                  userid=F('discordid__discord_id'))

    return users

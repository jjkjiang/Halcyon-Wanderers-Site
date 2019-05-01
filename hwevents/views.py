from django.shortcuts import render
from hwevents.models import Event
from django.db.models import Count
import datetime

# Create your views here.


def index(request):
    newest_events = Event.objects \
                        .filter(event_date__gt=datetime.datetime.now()) \
                        .annotate(going=Count('participants')) \
                        .order_by('event_date')[:10]

    return render(request, 'index.html', context={'newest_events': newest_events})

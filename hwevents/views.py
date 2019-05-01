from django.shortcuts import render
from hwevents.models import Event, Participant
from django.db.models import Count

# Create your views here.


def index(request):
    newest_events = Event.objects.all() \
                        .annotate(going=Count('participants')) \
                        .order_by('-event_date')[:10]

    return render(request, 'index.html', context={'newest_events': newest_events})

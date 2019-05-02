from django.forms import ModelForm, DateTimeField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from hwevents.models import Event
from django.db.models import Count
import datetime
from tempus_dominus.widgets import DateTimePicker

# Create your views here.


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

    newest_events = Event.objects \
                        .filter(event_date__gt=datetime.datetime.now()) \
                        .annotate(going=Count('participants')) \
                        .order_by('event_date')[:10]

    create_form = EventCreateForm()

    return render(request, 'index.html', context={'newest_events': newest_events, 'form': create_form})

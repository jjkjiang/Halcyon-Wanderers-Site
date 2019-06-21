from django.contrib import admin
from hwevents.models import *

# Register your models here.

admin.site.register(Participant)


class ParticipantInline(admin.TabularInline):
    model = Participant


class EventAdmin(admin.ModelAdmin):
    inlines = [
        ParticipantInline,
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(Game)
admin.site.register(Role)

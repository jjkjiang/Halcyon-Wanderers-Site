from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='page_index'),
    path('create/', views.create_event_view, name='create_event'),
    path('all/<int:page>/', views.all_events_view, name='all_events'),
    path('id/<slug:slug>-<int:id>/', views.detail_view, name="detail"),
    path('calendar/', views.calendar_view, name='calendar'),
    path('month/<str:start>/<str:end>/', views.get_month_events, name='get_month_events'),
    path('attendance/going/', views.attend, name='attend'),
    path('attendance/cancel/', views.cancel, name='cancel'),
    path('participants/', views.get_participants, name='get_participants'),
    path('event/', views.get_events, name='get_events')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attendance/going/', views.attend, name='attend'),
    path('attendance/cancel/', views.cancel, name='cancel'),
    path('participants/', views.get_participants, name='get_participants')
]
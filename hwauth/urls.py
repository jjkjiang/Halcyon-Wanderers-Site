from django.urls import path
from . import views

urlpatterns = [
    path('discord/', views.oauth_redirect, name='oauth_redirect'),
]
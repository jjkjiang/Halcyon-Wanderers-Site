from django.urls import path

from . import views

urlpatterns = [
    path('discord/', views.oauth_redirect, name='oauth_redirect'),
    path('logout/', views.logout_view, name='logout'),
    path('change/', views.change_username, name='change'),
]
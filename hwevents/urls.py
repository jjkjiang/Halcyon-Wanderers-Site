from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index'),
    path('all/<int:page>/', views.all_view, name='past_view'),
    path('id/<int:id>/', views.detail_view, name="detail_view"),
    path('attendance/going/', views.attend, name='attend'),
    path('attendance/cancel/', views.cancel, name='cancel'),
    path('participants/', views.get_participants, name='get_participants'),
    path('event/', views.get_events, name='get_events')
]

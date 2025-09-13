from django.urls import path
from . import views

urlpatterns = [
    path('room_select/', views.room_select ,name='room_select'),
]
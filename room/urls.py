from django.urls import path
from . import views

urlpatterns = [
    path('room_views/', views.room_view ,name='room_view')
]
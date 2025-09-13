from django.urls import path
from . import views

urlpatterns = [
    path('room<int:room_number>/', views.booking_view, name='booking_view'),
]
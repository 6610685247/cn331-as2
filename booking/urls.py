from django.urls import path
from . import views


urlpatterns = [
    path('/booking/room<int:room_number>/', views.booking_page, name='booking_page'),
    path('my_booking/', views.my_booking, name='my_booking'),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
]
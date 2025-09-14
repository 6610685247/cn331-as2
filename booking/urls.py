from django.urls import path
from . import views


urlpatterns = [
    path('room<int:room_number>/', views.booking_view, name='booking_view'),
    path('my_booking/', views.my_booking, name='my_booking'),
    path('booking_page/', views.booking_page, name='booking_page'),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path('booking_page/<int:room_id>/', views.booking_page, name='booking_page'),
]
from django.urls import path
from . import views
from booking import views as booking_views
urlpatterns = [
    path('floor/<int:floor>/', views.floor_rooms, name='floor_rooms'),
    path('booking_page/<int:room_id>/', booking_views.booking_page, name='booking_page')
]
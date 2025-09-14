from django.db import models
from room.models import Room
from accounts.models import Profile
from django.contrib.auth.models import User


class Booking(models.Model) :
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_id} is booked by { self.user } ({self.start_time} - {self.end_time})"
from django.db import models
from room.models import Room

# Create your models here.

class Booking(models.Model) :
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # User
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_id} is booked by UserX ({self.start_time} - {self.end_time})"
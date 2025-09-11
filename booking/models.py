from django.db import models
from room.models import Room

# Create your models here.

class Booking(models.Model) :
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # User
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
from django.db import models

# Create your models here.
class Room(models.Model) :
    room_id = models.CharField(max_length=3, primary_key=True)
    room_name = models.CharField(max_length=50)
    cap = models.IntegerField()
    bookable = models.BooleanField(default=True)
    status = models.BooleanField(default=False)

    def get_status(self):
        return "On" if self.status else "Off"
    
class Booking(models.Model) :
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # User
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
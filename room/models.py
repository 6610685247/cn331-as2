from django.db import models


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=50, null=False)
    cap = models.IntegerField(null=True, blank=True)
    floor = models.IntegerField()
    status = models.BooleanField(default=False)


    def get_status(self):
        return "On" if self.status else "Off"
    def __str__(self):
        return self.room_name

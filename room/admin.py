from django.contrib import admin
from .models import Room
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_id", "room_name", "cap", "floor", "get_status")
    list_filter = ("status", "floor")
    search_fields = ("room_name", "room_id")
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room
from collections import defaultdict

# Create your views here.

@login_required(login_url='login')
def room_select(request):
    rooms = Room.objects.all().order_by('floor', 'room_name')

    # Serialize rooms into JSON-friendly dict
    rooms_by_floor = {}
    for room in rooms:
        rooms_by_floor.setdefault(room.floor, []).append({
            "room_id": room.room_id,
            "room_name": room.room_name
        })

    if request.method == "POST":
        selected_room = request.POST.get("selected_room")
        if selected_room:
            return redirect(f"/room{selected_room}/")

    return render(request, "room/room_select.html", {"rooms_by_floor": rooms_by_floor})
        
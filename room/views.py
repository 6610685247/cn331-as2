from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room

# Create your views here.

@login_required(login_url='login')
def room_select(request):
    rooms = Room.objects.all()
    if request.method == "POST":
        selected_room = request.POST.get("selected_room")
        if selected_room:
            return redirect(f"/room{selected_room}/")
    return render(request, "room/room_select.html", {"rooms": rooms})
        
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def room_select(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "room_select":
            room = request.POST.get("selected_room")
            return redirect("booking_view", room_number=room)
    return render(request, "room/room_select.html")
    
        
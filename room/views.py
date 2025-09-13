from django.shortcuts import render, redirect

# Create your views here.

def room_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "room_select":
            room = request.POST.get("selected_room")
            return redirect("booking_view", room_number=room)
    return render(request, "room/room_select.html")
    
        
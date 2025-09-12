from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from datetime import datetime
from room.models import Room
from booking.models import Booking

# Create your views here.
def booking_view(request):
    return render(request, "booking/booking_page.html")

def main_page(request):
    return render(request, "booking_web/index.html")

def book_room(request):
    if request.method == "POST":

        id = request.POST.get("room_id")
        date = request.POST.get("date")
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")

        room = Room.objects.get(room_id=id)

        start_date = make_aware(datetime.fromisoformat(f"{date}T{start}"))
        end_date = make_aware(datetime.fromisoformat(f"{date}T{end}"))

        overlap = Booking.objects.filter(
            room=room,
            start_time__lt=end_date,
            end_time__gt=start_date,
        ).exists()

        if overlap:
            return redirect('booking')
        Booking.objects.create(room_id=id, start_time=start_date, end_time=end_date)
        return redirect('booking') 
    else:
        return render(request, "booking/booking_page.html") #Safety first
    
def get_date(request):
    if request.method == "POST":
        date = request.POST.get("selectedDate")
        request.session["selected_date"] = date  
        return render(request, 'booking/booking_page.html', {'selected_date' : date})
    
# def room_select(request):
#     if request.method == "POST":
#         room = request.POST.get("selected_room")
#         return render(request, 'booking/booking_page.html', {'selected_room' : room})
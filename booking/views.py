from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime, date
from room.models import Room
from booking.models import Booking

# Create your views here.
def booking_view(request, room_number): #everything about req in booking view
    
    context = {
            "room_num" : room_number,
            "booking_date" : timezone.localdate().strftime("%Y-%m-%d")
            }
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "set_date":
            request.session["booking_date"] = request.POST.get("booking_date")
            context = {
                "room_num" : room_number,
                "booking_date" : request.session["booking_date"]
                }
        elif action == "book":
            current_user = request.user
            book_date = request.POST.get("date")
            start = request.POST.get("start_time")
            end = request.POST.get("end_time")

            room = Room.objects.get(room_id=room_number)

            start_date = make_aware(datetime.fromisoformat(f"{book_date}T{start}"))
            end_date = make_aware(datetime.fromisoformat(f"{book_date}T{end}"))

            overlap_room = Booking.objects.filter(
                room=room,
                user_id=current_user,
            ).exists()

            overlap_book = Booking.objects.filter(
                room=room,
                start_time__lt=end_date,
                end_time__gt=start_date,
            ).exists()

            if overlap_room or overlap_book:
                return render(request, "booking/booking_page.html", context)
            Booking.objects.create(room_id=room_number, user=current_user, start_time=start_date, end_time=end_date)
        
    return render(request, "booking/booking_page.html", context)

# def get_date(request, room_number):
#     if request.method == "POST":
#         date = request.POST.get("selectedDate")
#         request.session["selected_date"] = date  
#         return render(request, 'booking/booking_page.html', {'selected_date' : date , "room_num" : room_number}, )

def book_room(request, room_number):
    if request.method == "POST":
        id = room_number
        current_user = request.user
        date = request.POST.get("date")
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")

        room = Room.objects.get(room_id=id)

        start_date = make_aware(datetime.fromisoformat(f"{date}T{start}"))
        end_date = make_aware(datetime.fromisoformat(f"{date}T{end}"))

        overlap = Booking.objects.filter(
            room=room,
            user=current_user,
            start_time__lt=end_date,
            end_time__gt=start_date,
        ).exists()

        if overlap:
            return redirect('booking')
        Booking.objects.create(room_id=id, user=current_user, start_time=start_date, end_time=end_date)
        return redirect('') 
    else:
        return render(request, "booking/booking_page.html") #Safety first
    

    
# def room_select(request):
#     if request.method == "POST":
#         room = request.POST.get("selected_room")
#         return render(request, 'booking/booking_page.html', {'selected_room' : room})

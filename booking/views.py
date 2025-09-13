from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime, timedelta
from room.models import Room
from booking.models import Booking
from django.contrib.auth.decorators import login_required

# Create your views here.
def booking_view(request, room_number): #everything about req in booking view
    tmr =  timezone.localdate()+ timedelta(days=1)

    time_slot = [
        ('09:00:00', '10:00:00'),
        ('10:00:00', '11:00:00'),
        ('11:00:00', '12:00:00'),
        ('12:00:00', '13:00:00'),
        ('13:00:00', '14:00:00'),
        ]
    
    context = {
            "room_num" : room_number,
            "booking_date" : timezone.localdate().strftime("%Y-%m-%d"),
            "tmr" : tmr.strftime("%Y-%m-%d"),
            "book_date" : timezone.localdate().strftime("%Y-%m-%d"),
            "time_slot" : time_slot,
            }
        
    room_exist = Room.objects.filter(room_id=room_number).exists()
    if not room_exist:
        return redirect("room_view")
    


    if request.method == "POST":
        action = request.POST.get("action")
        if action == "book_today":
            context = {
            "room_num" : room_number,
            "booking_date" : timezone.localdate().strftime("%Y-%m-%d"),
            "tmr" : tmr.strftime("%Y-%m-%d"),
            "book_date" : request.POST.get("book_today"),
            "time_slot" : time_slot,
            }
        elif action == "book_tmr":
            context = {
            "room_num" : room_number,
            "booking_date" : timezone.localdate().strftime("%Y-%m-%d"),
            "tmr" : tmr.strftime("%Y-%m-%d"),
            "book_date" : request.POST.get("book_today"),
            "time_slot" : time_slot,
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

@login_required(login_url='login')
def my_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "booking/my_booking.html", {"bookings": bookings})

@login_required(login_url='login')
def booking_page(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "booking/booking_page.html", {"bookings": bookings})
    


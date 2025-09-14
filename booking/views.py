from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime, timedelta
from room.models import Room
from booking.models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def booking_view(request, room_number):
    today = timezone.localdate()
    tmr = today + timedelta(days=1)

    time_slot = [
        ('09:00:00', '10:00:00'),
        ('10:00:00', '11:00:00'),
        ('11:00:00', '12:00:00'),
        ('12:00:00', '13:00:00'),
        ('13:00:00', '14:00:00'),
    ]

    if not Room.objects.filter(room_id=room_number).exists():
        return redirect("room_view")

    book_date = today

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "book_today":
            book_date = today
        elif action == "book_tmr":
            book_date = tmr
        elif action == "book":

            book_date_str = request.POST.get("date")
            book_date = datetime.fromisoformat(book_date_str).date()

            start = request.POST.get("start_time")[:5]  
            end = request.POST.get("end_time")[:5]      

            start_dt = make_aware(datetime.combine(book_date, datetime.strptime(start, "%H:%M").time()))
            end_dt = make_aware(datetime.combine(book_date, datetime.strptime(end, "%H:%M").time()))
            room = Room.objects.get(room_id=room_number)

            if Booking.objects.filter(user=request.user,room_id = room_number, start_time__date=book_date).exists():
                messages.error(request, f"You already booked on {book_date}.")

            elif Booking.objects.filter(room=room, start_time__lt=end_dt, end_time__gt=start_dt).exists():
                messages.error(request, "This slot is already booked.")
            else:
                Booking.objects.create(
                    room=room,
                    user=request.user,
                    start_time=start_dt,
                    end_time=end_dt,
                    room_id=room_number,
                )
                messages.success(request, f"Booking confirmed for {book_date} {start}-{end}.")

    booked_slots = Booking.objects.filter(
        room_id=room_number,
        start_time__date=book_date
    ).values_list('start_time', 'end_time')

    booked_slots = [(b[0].strftime("%H:%M"), b[1].strftime("%H:%M")) for b in booked_slots]

    # list slot ของ user ที่จองแล้ว
    user_booked_slots = Booking.objects.filter(
        user=request.user,
        start_time__date=book_date,
        room_id=room_number
        ).values_list('start_time', 'end_time')

    user_booked_slots = [(b[0].strftime("%H:%M"), b[1].strftime("%H:%M")) for b in user_booked_slots]

    slots_info = []
    for start, end in time_slot:
        start_short, end_short = start[:5], end[:5]
        # เช็คว่า slot นี้ถูกจองหรือไม่
        is_booked = (start_short, end_short) in booked_slots or (start_short, end_short) in user_booked_slots
        slots_info.append({
            "start": start_short,
            "end": end_short,
            "room_id": room_number,
            "is_booked": is_booked
        })


    context = {
        "room_id": room_number,
        "book_date": book_date.strftime("%Y-%m-%d"),
        "today": today.strftime("%Y-%m-%d"),
        "tmr": tmr.strftime("%Y-%m-%d"),
        "slots_info": slots_info,
        "room_name": Room.objects.get(room_id=room_number).room_name,
        "room_status": Room.objects.get(room_id=room_number).status,
    }

    return render(request, "booking/booking_page.html", context)

@login_required(login_url='login')
def my_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    now = timezone.now()
    return render(request, "booking/my_booking.html", {"bookings": bookings, "now": now})

@login_required(login_url='login')
def booking_page(request):
    bookings = Booking.objects.filter(user=request.user)
    now = timezone.now()
    return render(request, "booking/booking_page.html", {"bookings": bookings, "now": now})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my_booking')
    


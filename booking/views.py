from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime, timedelta
from room.models import Room
from booking.models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import localdate


@login_required
def booking_page(request, room_number):
    today = localdate()
    tmr = today + timedelta(days=1)

    time_slots = [
        ('09:00:00', '10:00:00'),
        ('10:00:00', '11:00:00'),
        ('11:00:00', '12:00:00'),
        ('12:00:00', '13:00:00'),
        ('13:00:00', '14:00:00'),
    ]

    try:
        room = Room.objects.get(room_id=room_number)
    except Room.DoesNotExist:
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
            start_time_str = request.POST.get("start_time")[:5]
            end_time_str = request.POST.get("end_time")[:5]

            start_dt = make_aware(datetime.combine(book_date, datetime.strptime(start_time_str, "%H:%M").time()))
            end_dt = make_aware(datetime.combine(book_date, datetime.strptime(end_time_str, "%H:%M").time()))

            if Booking.objects.filter(room=room, start_time__lt=end_dt, end_time__gt=start_dt).exists():
                messages.error(request, "This slot is already booked.")
            else:
                Booking.objects.create(
                    room=room,
                    user=request.user,
                    start_time=start_dt,
                    end_time=end_dt
                )
                messages.success(request, f"Booking confirmed for {book_date} {start_time_str}-{end_time_str}.")

    slots_info = []
    for start_str, end_str in time_slots:
        start_dt = make_aware(datetime.combine(book_date, datetime.strptime(start_str[:5], "%H:%M").time()))
        end_dt = make_aware(datetime.combine(book_date, datetime.strptime(end_str[:5], "%H:%M").time()))
        is_booked = Booking.objects.filter(room=room, start_time__lt=end_dt, end_time__gt=start_dt).exists()
        slots_info.append({
            "start": start_str[:5],
            "end": end_str[:5],
            "room_id": room_number,
            "is_booked": is_booked
        })

    context = {
        "room_id": room_number,
        "book_date": book_date.strftime("%Y-%m-%d"),
        "today": today.strftime("%Y-%m-%d"),
        "tmr": tmr.strftime("%Y-%m-%d"),
        "slots_info": slots_info,
        "room_name": room.room_name,
        "room_status": room.status,
    }

    return render(request, "booking/booking_page.html", context)

@login_required(login_url='login')
def my_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    now = timezone.now()
    return render(request, "booking/my_booking.html", {"bookings": bookings, "now": now})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my_booking')
    


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from booking.models import Booking
from room.models import Room
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.contrib import messages


def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    floors_data = []
    floor_numbers = Room.objects.values_list('floor', flat=True).distinct()
    for f in floor_numbers:
        available_count = Room.objects.filter(floor=f, status=True).count()
        floors_data.append({'floor': f, 'available_rooms': available_count})
    
    context = {
        'floors': floors_data
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    next_page = request.GET.get('next', 'home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.POST.get('next') or 'home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password', 'next': next_page})
    return render(request, 'login.html', {'next': next_page})

def logout_view(request):
    logout(request)
    return redirect('home')

@user_passes_test(lambda u: u.is_staff, login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.all().select_related("room", "user")
    users = User.objects.all()

    user_id = request.GET.get("user")
    room_id = request.GET.get("room")
    date_str = request.GET.get("date")
    start = request.GET.get("start")
    end = request.GET.get("end")
    start_hours = ["09:00", "10:00", "11:00", "12:00", "13:00"]
    end_hours = ["10:00", "11:00", "12:00", "13:00", "14:00"]

    if user_id:
        bookings = bookings.filter(user__id=user_id)
    if room_id:
        bookings = bookings.filter(room__room_id=room_id)
    if date_str:
        date_obj = parse_date(date_str)
        bookings = bookings.filter(start_time__date=date_obj)
    if start:
        start_hour = int(start.split(":")[0])
        bookings = bookings.filter(start_time__hour__gte=start_hour)
    if end:
        end_hour = int(end.split(":")[0])
        bookings = bookings.filter(end_time__hour__lte=end_hour)

    if request.method == "POST":
        if "add_room" in request.POST:
            room_id = request.POST.get("room_id")
            room_name = request.POST.get("room_name")
            cap = request.POST.get("cap")
            floor = room_id[0]

            if not room_name:
                room_name = room_id

            Room.objects.create(
                room_id=room_id,
                room_name=room_name,
                cap=int(cap) if cap else None,
                floor=floor
            )
            messages.success(request, f"Room {room_id} added successfully.")

        elif "delete_room" in request.POST:
            room_id = request.POST.get("room_id")
            Room.objects.filter(room_id=room_id).delete()
            messages.success(request, f"Room {room_id} deleted successfully.")
        elif "status_to_on" in request.POST:
            room_id = request.POST.get("room_id")
            Room.objects.filter(room_id=room_id).update(status=True)
            messages.success(request, f"Room {room_id} set to ON.")
        elif "status_to_off" in request.POST:
            room_id = request.POST.get("room_id")
            Room.objects.filter(room_id=room_id).update(status=False)
            messages.success(request, f"Room {room_id} set to OFF.")

    
    context = {
        "rooms": rooms,
        "bookings": bookings,
        "users": users,
        "request": request,
        "start_hours": start_hours,
        "end_hours": end_hours,
    }
    return render(request, "dashboard.html", context)



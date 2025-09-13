from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from booking.models import Booking

def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    return render(request, 'home.html')

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

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@user_passes_test(lambda u: u.is_staff, login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    bookings = Booking.objects.all().select_related("room", "user")


    start = request.GET.get("start")
    end = request.GET.get("end")

    if start:
        bookings = bookings.filter(start_time__gte=start)
    if end:
        bookings = bookings.filter(end_time__lte=end)

    return render(request, "dashboard.html", {"bookings": bookings})


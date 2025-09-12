from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
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

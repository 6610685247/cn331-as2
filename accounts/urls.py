from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/booking/', views.admin_booking_list, name='admin_booking_list'),
    path('dashboard/booking/filter/', views.admin_booking_filter, name='admin_booking_filter'),
]

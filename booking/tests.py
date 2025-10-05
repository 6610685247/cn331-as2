from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import Profile,Booking,Room
from datetime import datetime, date, timedelta
from django.urls import reverse



class BookingTestCase(TestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "test"
        self.studentid = "123456789"
        self.date = date.today()
        self.start_time = "09:00"
        self.end_time = "10:00"

        self.user = User.objects.create_user(username=self.username, password=self.password)
        Profile.objects.create(user=self.user, studentid=self.studentid)
        self.room = Room.objects.create(room_id="999", room_name="test_room", cap=50, floor=9, status=True)

        self.data = {
            "action": "book",
            "date": self.date.isoformat(),
            "start_time": self.start_time,
            "end_time": self.end_time
        }


    def test_booking_success(self):
        self.start_time_value = datetime.strptime("09:00", "%H:%M").time()
        self.end_time_value = datetime.strptime("10:00", "%H:%M").time()

        booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            start_time=datetime.combine(self.date, self.start_time_value),
            end_time=datetime.combine(self.date, self.end_time_value)
        )

        
        self.assertEqual(Booking.objects.count(), 1)

       
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.start_time.time(), self.start_time_value)
        self.assertEqual(booking.end_time.time(), self.end_time_value)
    
    def test_user_book_same_slot_same_day(self):
        
        self.client.login(username=self.username, password=self.password)

        
        response1 = self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)

        
        response2 = self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)
        self.assertEqual(Booking.objects.count(), 1)  
        self.assertContains(response2, "already booked", status_code=200)

    def test_two_users_booking_same_slot(self):
        
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)
        self.assertEqual(Booking.objects.count(), 1)
        self.client.logout()

        
        self.username2 = "test_user_2"
        self.password2 = "test2"
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        Profile.objects.create(user=self.user2, studentid="234567890")

        
        self.client.login(username=self.username2, password=self.password2)
        response2 = self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)

        
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response2, "already booked", status_code=200)

    def test_user_book_two_time_slots_same_day(self):
        self.client.login(username=self.username, password=self.password)

        
        response1 = self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response1,f"Booking confirmed for {self.date} {self.start_time}-{self.end_time}",status_code=200)

        second_data = {
            "action": "book",
            "date": self.date,
            "start_time": "10:00",
            "end_time": "11:00",
        }
        
        response2 = self.client.post(reverse("booking_page", args=[self.room.room_id]), second_data)

       
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response2, f"You already booked on {self.date}", status_code=200)

    def test_user_book_same_time_two_days(self):
        self.client.login(username=self.username, password=self.password)

       
        response1 = self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response1,f"Booking confirmed for {self.date} {self.start_time}-{self.end_time}",status_code=200)


        
        tmr_date = (date.today() + timedelta(days=1)).isoformat()
        second_data = {
            "action": "book",
            "date": tmr_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
        response2 = self.client.post(reverse("booking_page", args=[self.room.room_id]), second_data)

        
        self.assertContains(response2,f"Booking confirmed for {tmr_date} {self.start_time}-{self.end_time}",status_code=200)
        self.assertEqual(Booking.objects.count(), 2)

    def test_cancel_booking(self):
        self.client.login(username=self.username, password=self.password) 

       
        response1 = self.client.post(reverse("booking_page", args=[self.room.room_id]), self.data)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response1,f"Booking confirmed for {self.date} {self.start_time}-{self.end_time}",status_code=200)

        booking = Booking.objects.first() 

       
        response2 = self.client.post(reverse("cancel_booking", args=[booking.id]))
        
        self.assertEqual(Booking.objects.count(), 0) 
        self.assertRedirects(response2, reverse("my_booking")) 


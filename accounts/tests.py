from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from room.models import Room
from django.test import TestCase, Client
from django.contrib.messages import get_messages
import io
import sys


class ProfileModelTest(TestCase):
    def test_str_method(self):
        user = User.objects.create(username="testuser2")
        profile = Profile.objects.create(user=user, studentid="2222222222")
        self.assertEqual(str(profile), "testuser2 (2222222222)")

class AccountsTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.studentid = "1234567890"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        Profile.objects.create(user=self.user, studentid=self.studentid)
    
    def test_register_success(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password": "newpassword",
            "studentid": "1111111111",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Profile.objects.filter(studentid="1111111111").exists())

    def test_register_fail_duplicate_studentid(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            response = self.client.post(reverse("register"), {
                "username": "anotheruser",
                "password": "anotherpass",
                "studentid": self.studentid,
            })
        finally:
            sys.stdout = old_stdout
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="anotheruser").exists())
        self.assertEqual(Profile.objects.filter(studentid=self.studentid).count(), 1)

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_fail(self):
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        response = self.client.get(reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class AdminDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.room_id = 999
        self.admin_user = User.objects.create_superuser(username="admin", password="pass", email="admin@example.com")
        self.client.login(username="admin", password="pass")

    def test_add_room(self):
        data = {
            "add_room": "1",         
            "room_id": self.room_id,
            "room_name": "Test Room",
            "cap": 50
        }
        response = self.client.post(reverse("dashboard"), data)
       
        room = Room.objects.get(room_id=self.room_id)
        self.assertEqual(room.room_name, "Test Room")
        self.assertEqual(room.cap, 50)
        self.assertEqual(room.floor, 9)  

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(f"Room {self.room_id} added successfully.")
    
    def test_delete_room(self):
        Room.objects.create(room_id=1000, room_name="Room Delete", cap=20, floor=1)
        data = {"delete_room": "1", "room_id": 1000}
        response = self.client.post(reverse("dashboard"), data)
        self.assertFalse(Room.objects.filter(room_id=1000).exists())
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Room 1000 deleted successfully.", messages)

    def test_status_on_off(self):
        Room.objects.create(room_id=2000, room_name="Room Status", cap=10, floor=2, status=False)

        response_on = self.client.post(reverse("dashboard"), {"status_to_on": "1", "room_id": 2000})
        room = Room.objects.get(room_id=2000)
        self.assertTrue(room.status)
        messages_on = [str(m) for m in get_messages(response_on.wsgi_request)]
        self.assertIn("Room 2000 set to ON.", messages_on)

        response_off = self.client.post(reverse("dashboard"), {"status_to_off": "1", "room_id": 2000})
        room.refresh_from_db()
        self.assertFalse(room.status)
        messages_off = [str(m) for m in get_messages(response_off.wsgi_request)]
        self.assertIn("Room 2000 set to OFF.", messages_off)




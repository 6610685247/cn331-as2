from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from room.models import Room
from django.test import TestCase, Client
from django.contrib.messages import get_messages
import io
import sys


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



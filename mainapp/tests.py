from django.test import TestCase
from .models import Appointment, Message, Realization, Comment

class AppointmentModelTest(TestCase):
    def test_str_representation(self):
        appointment = Appointment(description="Test Appointment", date="2024-05-21")

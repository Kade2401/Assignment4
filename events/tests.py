from django.test import TestCase
from .models import Event


class EventModelTest(TestCase):

    def test_event_creation(self):
        event = Event.objects.create(
            name="Test Event",
            date="2026-01-01",
            capacity=20
        )
        self.assertEqual(event.name, "Test Event")
        self.assertEqual(event.capacity, 20)


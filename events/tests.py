from django.test import TestCase
from .models import Event, Attendee
from django.db import IntegrityError
from datetime import date
from django.urls import reverse
from django.test import Client



class EventModelTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name="Django Conference",
            date=date.today(),
            capacity=2
        )

    def test_event_str(self):
        self.assertEqual(str(self.event), "Django Conference")

    def test_available_spots(self):
        self.assertEqual(self.event.available_spots(), 2)

        Attendee.objects.create(name="Alice", event=self.event)
        self.assertEqual(self.event.available_spots(), 1)

    def test_is_full(self):
        self.assertFalse(self.event.is_full())

        Attendee.objects.create(name="Alice", event=self.event)
        Attendee.objects.create(name="Bob", event=self.event)

        self.assertTrue(self.event.is_full())

class AttendeeModelTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name="Security Meetup",
            date=date.today(),
            capacity=10
        )

    def test_unique_attendee_per_event(self):
        Attendee.objects.create(name="Alice", event=self.event)

        with self.assertRaises(IntegrityError):
            Attendee.objects.create(name="Alice", event=self.event)


class EventViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            name="Blue Team Lab",
            date=date.today(),
            capacity=5
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('event_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blue Team Lab")


    def test_create_event(self):
        response = self.client.post(reverse('create_event'), {
            'name': 'New Event',
            'date': '2026-01-01',
            'capacity': 10
        })

        self.assertEqual(Event.objects.count(), 2)
        self.assertRedirects(response, reverse('event_list'))

class AttendeeRegistrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            name="AppSec Workshop",
            date=date.today(),
            capacity=1
        )

    def test_register_attendee_success(self):
        response = self.client.post(
            reverse('register_attendee', args=[self.event.id]),
            {'name': 'Alice'}
        )

        self.assertEqual(Attendee.objects.count(), 1)
        self.assertRedirects(
            response,
            reverse('event_detail', args=[self.event.id])
        )

    def test_cannot_register_when_event_is_full(self):
        Attendee.objects.create(name="Alice", event=self.event)

        response = self.client.post(
            reverse('register_attendee', args=[self.event.id]),
            {'name': 'Bob'}
        )

        self.assertEqual(Attendee.objects.count(), 1)

    def test_cannot_register_same_attendee_twice(self):
        self.client.post(
            reverse('register_attendee', args=[self.event.id]),
            {'name': 'Alice'}
        )

        self.client.post(
            reverse('register_attendee', args=[self.event.id]),
            {'name': 'Alice'}
        )

        self.assertEqual(Attendee.objects.count(), 1)

class DeleteEventSecurityTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            name="Critical Event",
            date=date.today(),
            capacity=10
        )

    def test_delete_event_get_not_allowed(self):
        response = self.client.get(
            reverse('delete_event', args=[self.event.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(id=self.event.id).exists())

#fjgbdkfuhsfsdoj

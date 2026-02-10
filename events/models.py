from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

class Event(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events'
    )

    invited_users = models.ManyToManyField(
        User,
        related_name='invited_events',
        blank=True
    )
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    location_name = models.CharField(max_length=200, blank=True)
    location_address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, blank=True)
    description = models.TextField(blank=True)

    is_global = models.BooleanField(default=False)

    invite_only = models.BooleanField(default=False)

    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.name

    def available_spots(self):
        return self.capacity - self.attendees.count()

    def is_full(self):
        return self.attendees.count() >= self.capacity


class Attendee(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True)
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'event')

    def __str__(self):
        return f"{self.name} - {self.role} ({self.event.name})"
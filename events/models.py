from django.db import models

# Create your models here.
# events/models.py
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def available_spots(self):
        return self.capacity - self.attendees.count()

    def is_full(self):
        return self.attendees.count() >= self.capacity

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'event')  # чтобы избежать дубликатов

    def __str__(self):
        return f"{self.name} ({self.event.name})"
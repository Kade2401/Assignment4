
from django import forms
from .models import Event, Attendee

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'capacity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name']
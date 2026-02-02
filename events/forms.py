
from django import forms
from .models import Event, Attendee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
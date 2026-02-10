
from django import forms
from .models import Event, Attendee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    VISIBILITY_CHOICES = [
        ("none", "Normal"),
        ("invite", "Private (invite-only)"),
        ("global", "Global"),
    ]

    visibility = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        initial="none",
        label="Event type",
    )

    class Meta:
        model = Event
        fields = [
            'name',
            'date',
            'capacity',
            'location_name',
            'location_address',
            'latitude',
            'longitude', 
            "description"
        ]
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if instance:
            if getattr(instance, "is_global", False):
                self.fields["visibility"].initial = "global"
            elif getattr(instance, "invite_only", False):
                self.fields["visibility"].initial = "invite"
            else:
                self.fields["visibility"].initial = "none"


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'role']
        widgets = {
            'role': forms.TextInput(attrs={
                'placeholder': 'например: guest / speaker / VIP',
                'class': 'form-control'
            })
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class AttendeeRoleForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['role']
        widgets = {
            'role': forms.TextInput(attrs={
                'placeholder': 'New role',
                'class': 'form-control'
            })
        }

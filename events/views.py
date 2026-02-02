from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Attendee
from .forms import EventForm, AttendeeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


def event_list(request):
    events = Event.objects.all()
    return render(request, 'registration/register.html', {'events': events})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.error(request, f"Event '{event_name}' has been deleted.")
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'event': event})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = event.attendees.all()
    form = AttendeeForm()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'attendees': attendees,
        'form': form,
        'is_full': event.is_full()
    })


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            new_capacity = form.cleaned_data['capacity']
            if new_capacity < event.attendees.count():
                messages.error(request, "Cannot reduce capacity below current number of attendees!")
            else:
                form.save()
                messages.success(request, "Event updated!")
                return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

@login_required
def register_attendee(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if event.is_full():
                messages.error(request, "Cannot register. Event is full!")
            elif Attendee.objects.filter(name=name, event=event).exists():
                messages.warning(request, f"{name} is already registered.")
            else:
                Attendee.objects.create(name=name, event=event)
                messages.info(request, f"{name} successfully registered!")
    return redirect('event_detail', event_id=event.id)

@login_required
def remove_attendee(request, attendee_id):
    attendee = get_object_or_404(Attendee, id=attendee_id)
    event_id = attendee.event.id
    attendee.delete()
    messages.info(request, f"Attendee removed from {attendee.event.name}.")
    return redirect('event_detail', event_id=event_id)

def api_event_list(request):
    if request.method == 'GET':
        events = Event.objects.all().values(
            'id', 'name', 'date', 'capacity'
        )
        return JsonResponse(list(events), safe=False)


@csrf_exempt
def api_create_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = Event.objects.create(
            name=data['name'],
            date=data['date'],
            capacity=data['capacity']
        )
        return JsonResponse({
            'status': 'created',
            'event_id': event.id
        })

def api_update_event(request, event_id):
    if request.method == "PUT":
        body = json.loads(request.body)
        event = get_object_or_404(Event, id=event_id)

        event.name = body.get("name", event.name)
        event.date = body.get("date", event.date)
        event.capacity = body.get("capacity", event.capacity)

        event.save()
        return JsonResponse({"status": "updated"})

def api_delete_event(request, event_id):
    if request.method == "DELETE":
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({"status": "deleted"})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("event_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    user = request.user
    events = []
    context = {
        'user': user,
        'events': events
    }
    return render(request, 'events/profile.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import logout
from django.db import models
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    events = Event.objects.filter(owner=request.user).order_by('start_time')
    return render(request, 'linkup/dashboard.html', {
        'user': request.user,
        'events': events
    })


def home(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(
            models.Q(owner=request.user) | models.Q(participants=request.user)
        ).order_by('start_time').distinct()
    else:
        events = Event.objects.none()
    return render(request, 'linkup/home.html', {'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'linkup/create_event.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, owner=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm(instance=event)
    return render(request, 'linkup/edit_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, owner=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'linkup/delete_event.html', {'event': event})



@login_required
def calendar_events(request):
    user_events = Event.objects.filter(
        models.Q(owner=request.user) | models.Q(participants=request.user)
    ).distinct()

    data = [{
        'id': event.id,
        'title': event.title,
        'start': event.start_time.isoformat(),  # Format the date in ISO format
        'end': event.end_time.isoformat(),      # Format the date in ISO format
        'description': event.description,
    } for event in user_events]

    return JsonResponse(data, safe=False)


@login_required
def calendar_view(request):
    events = Event.objects.filter(owner=request.user)
    return render(request, 'linkup/calendar.html', {'events': events})


@login_required
def mypage(request):
    owned_events = Event.objects.filter(owner=request.user)
    participating_events = Event.objects.filter(participants=request.user)

    context = {
        'owned_events': owned_events,
        'participating_events': participating_events,
    }
    return render(request, 'linkup/mypage.html', context)



@login_required
def owned_events(request):
    events = Event.objects.filter(owner=request.user)
    return render(request, 'linkup/owned_events.html', {'events': events})


@login_required
def participating_events(request):
    events = Event.objects.filter(participants=request.user)
    return render(request, 'linkup/participating_events.html', {'events': events})


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponseForbidden("Invalid request method")
    

@login_required
def suggest_free_times(request):
    start_range = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end_range = start_range.replace(hour=20)

    busy_times = Event.objects.filter(
        Q(owner=request.user) | Q(participants=request.user),
        start_time__lt=end_range,
        end_time__gt=start_range
    ).values('start_time', 'end_time')

    busy = sorted([(e['start_time'], e['end_time']) for e in busy_times])
    cursor = start_range
    free_slots = []

    for start, end in busy:
        if cursor < start:
            free_slots.append((cursor, start))
        cursor = max(cursor, end)

    if cursor < end_range:
        free_slots.append((cursor, end_range))

    suggestions = [
        {"start": slot[0].isoformat(), "end": slot[1].isoformat()}
        for slot in free_slots if (slot[1] - slot[0]) >= timedelta(minutes=30)
    ]

    return JsonResponse(suggestions, safe=False)

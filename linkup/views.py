from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


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
            event.owner = request.user  # assign logged-in user as owner
            event.save()
            form.save_m2m()  # save participants
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

    data = []
    for event in user_events:
        data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
        })
    return JsonResponse(data, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'linkup/calendar.html')




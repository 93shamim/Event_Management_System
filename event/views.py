from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Event, Booking
from .forms import EventForm

def dashboard(request):
    return render(request, 'dashboard.html')

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event/event_list.html', {'events': events})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})

@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this event")
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event/update_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this event")
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event/delete_event.html', {'event': event})

# Booking part
def events_home(request):
    events = Event.objects.all()
    booked_events = Booking.objects.filter(user=request.user).values_list('event_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'events_home.html', {'events': events, 'booked_events': booked_events})

@login_required
def book_an_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    booking, created = Booking.objects.get_or_create(user=request.user, event=event)

    if created:
        messages.success(request, "Event booked successfully!")
    else:
        messages.info(request, "You have already booked this event.")

    return redirect('events_home')

@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user).select_related('event')
    return render(request, 'booked_events.html', {'bookings': bookings})

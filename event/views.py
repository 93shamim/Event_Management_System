from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .models import Event, Booking
from .forms import EventForm



# @login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
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


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.booked_by.add(request.user)
        return redirect('event_list')
    return render(request, 'event/book_event.html', {'event': event}) 


@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'event/booked_events.html', {'bookings': bookings})



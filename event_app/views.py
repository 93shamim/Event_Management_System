from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import EventApp, Booking
from category.models import Category
from .forms import EventAppForm
from django.utils import timezone
import pytz
from registration.models import CustomUser
from organizer.models import Organizer




def dashboard(request):
    total_users = CustomUser.objects.count()  
    total_events = EventApp.objects.count()
    total_categories = Category.objects.count() 
    total_organizers = Organizer.objects.count()
    ongoing_events = EventApp.objects.filter(start_date_time__lte=timezone.now(), end_date_time__gte=timezone.now()).count()  # Ongoing events
    start_soon_events = EventApp.objects.filter(start_date_time__gte=timezone.now()).count()  # Start soon events
    finished_events = EventApp.objects.filter(end_date_time__lt=timezone.now()).count()  # Finished events

    if request.user.is_authenticated:
        my_booked_events = Booking.objects.filter(user=request.user).count()
    else:
        my_booked_events = 0



    context = {
        'total_users': total_users,
        'total_events': total_events,
        'my_booked_events': my_booked_events,
        'total_categories': total_categories,
        'total_organizers': total_organizers,
        'ongoing_events': ongoing_events,
        'start_soon_events': start_soon_events,
        'finished_events': finished_events,
    }

    return render(request, 'dashboard.html', context)

    # return render(request, 'dashboard.html')




# def event_list(request):
#     events = EventApp.objects.all()
#     for event in events:
#         if request.user.is_authenticated:
#             event.is_booked = Booking.objects.filter(user=request.user, event=event).exists()
#         else:
#             event.is_booked = False
#         event.time_left = event.get_time_left()
#     return render(request, 'event_app/event_list.html', {'events': events})


# def event_list(request):
#     events = EventApp.objects.all()
#     current_time = timezone.now()
#     for event in events:
#         if request.user.is_authenticated:
#             event.is_booked = Booking.objects.filter(user=request.user, event=event).exists()
#         else:
#             event.is_booked = False

#         # Debug print for time left
#         time_left = event.get_time_left()
#         booked_quantity = event.get_booked_quantity()
#         available_quantity = event.get_available_quantity()
#         print(f"Event: {event.name}, Start: {event.start_date_time}, Time Left: {time_left}, Booked: {booked_quantity}, Available: {available_quantity}")

#         # Optional: Add booked and available quantities to event object
#         event.booked_quantity = booked_quantity
#         event.available_quantity = available_quantity
#         event.is_fully_booked = event.is_fully_booked()

#     return render(request, 'event_app/event_list.html', {'events': events, 'current_time': current_time})

# event views
def event_list(request):
    events = EventApp.objects.all()
    for event in events:
        if request.user.is_authenticated:
            event.is_booked = Booking.objects.filter(user=request.user, event=event).exists()
        else:
            event.is_booked = False

        # # Debug print for time left
        # time_left = event.get_time_left()
        # booked_seat = event.get_booked_seat()
        # available_seat = event.get_available_seat()
        
        # # Add booked and available quantities to event object
        # event.time_left = time_left
        # event.booked_seat = booked_seat
        # event.available_seat = available_seat
        # event.is_fully_booked = event.is_fully_booked()

    return render(request, 'event_app/event_list.html', {'events': events})




@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventAppForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # Ensure the start_date_time is aware
            start_date_time = form.cleaned_data['start_date_time']
            if start_date_time.tzinfo is None:  # Check if it's naive
                event.start_date_time = timezone.make_aware(start_date_time, timezone=pytz.timezone('Asia/Dhaka'))
            else:
                event.start_date_time = start_date_time  # It's already aware
            event.creator = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventAppForm()
    return render(request, 'event_app/create_event.html', {'form': form})

# @login_required
# def update_event(request, event_id):
#     event = get_object_or_404(EventApp, id=event_id)
#     if event.creator != request.user and not request.user.is_staff:
#         return HttpResponseForbidden("You cannot edit this event")
#     if request.method == 'POST':
#         form = EventAppForm(request.POST, instance=event)
#         if form.is_valid():
#             # Ensure the start_date_time is aware
#             start_date_time = form.cleaned_data['start_date_time']
#             if start_date_time.tzinfo is None:  # Check if it's naive
#                 event.start_date_time = timezone.make_aware(start_date_time, timezone=pytz.timezone('Asia/Dhaka'))
#             else:
#                 event.start_date_time = start_date_time  # It's already aware
#             form.save()
#             return redirect('event_list')
#     else:
#         form = EventAppForm(instance=event)
#     return render(request, 'event_app/update_event.html', {'form': form, 'event': event})

@login_required
def update_event(request, event_id):
    event = get_object_or_404(EventApp, id=event_id)
    
    # Restrict access to the creator or staff
    if event.creator != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this event")
    
    if request.method == 'POST':
        form = EventAppForm(request.POST, instance=event)
        
        if form.is_valid():
            # Get start_date_time from form, make it timezone-aware if necessary
            start_date_time = form.cleaned_data['start_date_time']
            if start_date_time.tzinfo is None:          # Check if it's naive
                event.start_date_time = timezone.make_aware(start_date_time, timezone=pytz.timezone('Asia/Dhaka'))
            else:
                event.start_date_time = start_date_time  # It's already aware

            # Explicitly save the event to ensure the updated start_date_time is saved
            event.save()
            return redirect('event_list')
    else:
        form = EventAppForm(instance=event)

    return render(request, 'event_app/update_event.html', {'form': form, 'event': event})




@login_required
def delete_event(request, event_id):
    event = get_object_or_404(EventApp, id=event_id)
    if event.creator != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this event")
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    
    return render(request, 'event_app/delete_event.html', {'event': event})


@login_required
def book_event(request, event_id):
    event = get_object_or_404(EventApp, id=event_id)

    if request.method == "POST":
        if Booking.objects.filter(user=request.user, event=event).exists():
            messages.error(request, "You have already booked this event.")
        else:
            Booking.objects.create(user=request.user, event=event)
            messages.success(request, "Event booked successfully!")
        return redirect('booked_events')

    return render(request, 'event_app/book_event_confirmation.html', {'event': event})


@login_required
def unbook_event(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "You have successfully unbooked the event.")
        return redirect('booked_events')

    return render(request, 'event_app/unbook_event_confirmation.html', {'booking': booking})


@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)

    context = {
        'events': [booking.event for booking in bookings],  # This ensures the template always gets 'event'
        'bookings': bookings,  # Only needed if you are using bookings separately
    }
    return render(request, 'event_app/booked_events.html', context)
    # return render(request, 'event_app/booked_events.html', {'bookings': bookings})

from django.db import models
from django.conf import settings
from django.utils import timezone
import pytz
from category.models import Category



class EventApp(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=150)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    capacity = models.IntegerField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organizer = models.ForeignKey('organizer.Organizer', on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.name
    
    def get_duration(self):
        """Calculates the event duration in hours."""
        duration = self.end_date_time - self.start_date_time
        return round(duration.total_seconds() / 3600, 2)


    def get_time_left(self):
            local_tz = pytz.timezone('Asia/Dhaka')
            now = timezone.now().astimezone(local_tz)
            
            if now < self.start_date_time:
                time_left = self.start_date_time.astimezone(local_tz) - now
                days, seconds = time_left.days, time_left.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                return f"{days}d {hours}h {minutes}m"
            return "Ongoing" if now < self.end_date_time else "Finished"

    def get_booked_seat(self):
        return Booking.objects.filter(event=self).count()

    def get_available_seat(self):
        return self.capacity - self.get_booked_seat()

    def is_fully_booked(self):
        return self.get_booked_seat() >= self.capacity

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(EventApp, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.event.name}"

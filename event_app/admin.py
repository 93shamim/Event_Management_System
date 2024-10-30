from django.contrib import admin

from .models import EventApp

# Register your models here.


@admin.register(EventApp)
class EventAppAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'start_date_time', 'end_date_time', 'created_at', 'capacity', 'location', 'organizer']
    list_filter = ['category']
    search_fields = ['name', 'category', 'description', 'start_date_time', 'end_date_time', 'created_at', 'capacity', 'location', 'organizer']
    readonly_fields = ['created_at']


from django.contrib import admin

from .models import Event

# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'start_date', 'end_date', 'created_at', 'capacity', 'location']
    list_filter = ['category']
    search_fields = ['name', 'category', 'description', 'start_date', 'end_date', 'created_at', 'capacity', 'location']
    readonly_fields = ['created_at']


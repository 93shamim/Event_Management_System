from django.urls import path
from . import views

urlpatterns = [
    # path('', views.event_list, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('event_list', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('unbook/<int:booking_id>/', views.unbook_event, name='unbook_event'),
    path('booked-events/', views.booked_events, name='booked_events'),
]

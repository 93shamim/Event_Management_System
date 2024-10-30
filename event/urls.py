from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('event_list', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('book/<int:event_id>/', views.book_an_event, name='book_an_event'),
    path('booked-events/', views.booked_events, name='booked_events'),
]

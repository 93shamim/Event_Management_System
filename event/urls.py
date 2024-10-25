from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('event_list', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('booked/', views.booked_events, name='booked_events'),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]

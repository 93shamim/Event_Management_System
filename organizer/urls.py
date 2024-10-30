from django.urls import path
from .import views


urlpatterns = [
    path('add-organizer/', views.add_organizer, name='add_organizer'),
    path('organizer-list/', views.organizer_list, name='organizer_list'),
    path('edit-organizer/<int:organizer_id>/', views.edit_organizer, name='edit_organizer'),
    path('delete-organizer/<int:organizer_id>/', views.delete_organizer, name='delete_organizer'),

]

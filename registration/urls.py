# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    #path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    #path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('profile_update/', profile_update, name='profile_update'),
    path('change-password/', change_password, name='change_password'),
    path('register_user_list/', register_user_list, name='register_user_list'),
    path('toggle_user_status/', toggle_user_status, name='toggle_user_status'),

]


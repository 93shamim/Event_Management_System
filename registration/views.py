from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm, CustomProfileUpadteForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash




# Home view
# def home(request):
#     return render(request, 'base.html')



# Dashboard view
# # @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')




#Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})



# Registration view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Add request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')




# for profile update and change password

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomProfileUpadteForm(request.POST, request.FILES, instance=request.user)  # Add request.FILES like photo
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile_update')
    else:
        form = CustomProfileUpadteForm(instance=request.user)
    
    return render(request, 'registration/profile_update.html', {'form': form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/change_password.html', {'form': form})
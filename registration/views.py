from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm, CustomProfileUpadteForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser
from django.contrib.auth.decorators import user_passes_test




# #Login view
# def login_view(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#             return redirect('dashboard')  # Redirect to dashboard after successful login
#         else:
#             messages.error(request, 'Invalid username or password.')
#     else:
#         form = CustomLoginForm()

#     return render(request, 'registration/login.html', {'form': form})


#Login view
def login_view(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('dashboard')  # Redirect to dashboard if user is already logged in


# # Registration view
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)  # Add request.FILES
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registration successful! You can now log in.')
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})


# Registration view
def register_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)  # Add request.FILES
            if form.is_valid():
                if CustomUser.objects.filter(username=form.cleaned_data['username']).exists():
                    messages.error(request, 'Username already exists!')
                else:
                    form.save()
                    messages.success(request, 'Registration successful! You can now log in.')
                    return redirect('login')
        else:
            form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})
    else:
        return redirect('dashboard')





# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')




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
@user_passes_test(lambda u: u.is_superuser)
def register_user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'registration/register_user_list.html', {'users': users})



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



# // for user status apply(active/deactive)

from django.http import JsonResponse
from django.contrib.auth.models import User

def toggle_user_status(request):
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return JsonResponse({'success': True, 'status': user.is_active})


from django.shortcuts import redirect


def home(request):
    if not request.user.is_authenticated:
        return redirect('event_list')
    else:
        return redirect('dashboard')
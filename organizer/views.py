from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Organizer
from .forms import OrganizerForm
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import user_passes_test


# Organizer views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def organizer_list(request):
    organizers = Organizer.objects.all()
    return render(request, 'organizer/organizer_list.html', {'organizers': organizers})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_organizer(request):
    if request.method == 'POST':
        form = OrganizerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organizer added successfully!')
            return redirect('organizer_list')
        else:
            messages.error(request, mark_safe('<span style="color: red;">Organizer already exists!</span>'))
    else:
        form = OrganizerForm()
    return redirect('organizer_list')  

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_organizer(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    if request.method == 'POST':
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organizer updated successfully!')
            return redirect('organizer_list')
    else:
        form = OrganizerForm(instance=organizer)
    return redirect('organizer_list')  


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_organizer(request, organizer_id):
    organizer = get_object_or_404(Organizer, pk=organizer_id)

    if request.method == 'POST':
        organizer.delete()  
        messages.success(request, 'Organizer Deleted successfully!')  
        return redirect('organizer_list')  
    
    # If not POST, render the confirmation template
    return render(request, 'organizer/delete_organizer.html', {'organizer': organizer})


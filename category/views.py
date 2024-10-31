from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CategoryForm
from django.utils.safestring import mark_safe


# Category views
@login_required 
@user_passes_test(lambda u: u.is_superuser)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
        else:
            messages.error(request, mark_safe('<span style="color: red;">Category already exists!</span>'))
    else:
        form = CategoryForm()
    return redirect('category_list')  

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return redirect('category_list')  


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        category.delete()  
        messages.success(request, 'Category Deleted successfully!')  
        return redirect('category_list')  
    
    # If not POST, render the confirmation template
    return render(request, 'category/delete_category.html', {'category': category})

# @require_POST
# def delete_category(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#     category.delete()  
#     messages.success(request, 'Category Deleted successfully!')  
#     return redirect('category_list')
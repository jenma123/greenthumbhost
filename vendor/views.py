from django.shortcuts import render,redirect

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.forms import CategoryForm, PlantItemForm
from menu.models import Category, PlantItem
from .models import  Vendor
from django.contrib import messages
from .forms import VendorForm
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404, HttpResponseRedirect
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def plantitems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    plantitems = PlantItem.objects.filter(vendor=vendor, category=category)
    context = {
        'plantitems': plantitems,
        'category': category,
    }
    return render(request, 'vendor/plantitems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_plant(request):
    if request.method == 'POST':
        form = PlantItemForm(request.POST, request.FILES)
        if form.is_valid():
            planttitle = form.cleaned_data['plant_title']
            plant = form.save(commit=False)
            plant.vendor = get_vendor(request)
            plant.slug = slugify(planttitle)
            form.save()
            messages.success(request, 'plant Item added successfully!')
            return redirect('plantitems_by_category', plant.category.id)
        else:
            print(form.errors)
    else:
        form = PlantItemForm()
        # modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_plant.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_plant(request, pk=None):
    plant = get_object_or_404(PlantItem, pk=pk)
    if request.method == 'POST':
        form = PlantItemForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            planttitle = form.cleaned_data['plant_title']
            plant = form.save(commit=False)
            plant.vendor = get_vendor(request)
            plant.slug = slugify(planttitle)
            form.save()
            messages.success(request, 'plant Item updated successfully!')
            return redirect('plantitems_by_category', plant.category.id)
        else:
            print(form.errors)

    else:
        form = PlantItemForm(instance=plant)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'plant': plant,
    }
    return render(request, 'vendor/edit_plant.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_plant(request, pk=None):
    plant = get_object_or_404(PlantItem, pk=pk)
    plant.delete()
    messages.success(request, 'plant Item has been deleted successfully!')
    return redirect('plantitems_by_category', plant.category.id)



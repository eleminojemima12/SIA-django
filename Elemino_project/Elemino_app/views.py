from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PerformanceForm
from .models import Performance


def pet_list(request):
    performances = Performance.objects.order_by('pet_name')
    return render(
        request,
        'Elemino_app/pet_list.html',
        {'performances': performances, 'active_page': 'management'},
    )


def index(request):
    performances = Performance.objects.order_by('pet_name')
    return render(
        request,
        'Elemino_app/home.html',
        {
            'total_pets': performances.count(),
            'active_page': 'home',
        },
    )


def dashboard(request):
    performances = Performance.objects.order_by('pet_name')
    total_pets = performances.count()
    unique_breeds = performances.values_list('breed', flat=True).distinct().count()
    latest_pet = performances.order_by('-date_registered').first()

    return render(
        request,
        'Elemino_app/dashboard.html',
        {
            'performances': performances,
            'total_pets': total_pets,
            'unique_breeds': unique_breeds,
            'latest_pet': latest_pet,
            'recent_pets': performances.order_by('-date_registered')[:4],
            'active_page': 'dashboard',
        },
    )


def pet_gallery(request):
    performances = Performance.objects.order_by('pet_name')
    return render(
        request,
        'Elemino_app/pet_gallery.html',
        {'performances': performances, 'total_pets': performances.count(), 'active_page': 'gallery'},
    )


def account_create(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(
        request,
        'Elemino_app/account_create.html',
        {'form': form, 'active_page': None},
    )


def pet_detail(request, pk):
    pet = get_object_or_404(Performance, pk=pk)
    return render(request, 'Elemino_app/pet_detail.html', {'pet': pet})


def pet_create(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = PerformanceForm()
    return render(request, 'Elemino_app/pet_form.html', {'form': form, 'title': 'Add Pet'})


def pet_update(request, pk):
    pet = get_object_or_404(Performance, pk=pk)
    if request.method == 'POST':
        form = PerformanceForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PerformanceForm(instance=pet)
    return render(request, 'Elemino_app/pet_form.html', {'form': form, 'title': 'Edit Pet', 'pet': pet})


def pet_delete(request, pk):
    pet = get_object_or_404(Performance, pk=pk)
    if request.method == 'POST':
        pet.delete()
        return redirect('pet_list')
    return render(request, 'Elemino_app/pet_confirm_delete.html', {'pet': pet})
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

from mvtproject import settings
from .models import Task, TaskApplication, Skill

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        # Basic checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created. Please log in.')
        return redirect('login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        messages.error(request, 'Invalid credentials.')
        return render(request, 'login.html')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    # UserProfile is auto-created via signal
    return render(request, 'profile.html')


import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from django.core.serializers.json import DjangoJSONEncoder


@login_required
def task_list_view(request):
    qs = Task.objects.filter(status='available')
    tasks_data = list(
        qs.values('id', 'title', 'latitude', 'longitude', 'location', 'payment')
    )
    return render(request, 'task_list.html', {
        'tasks': qs,  # pass QuerySet for HTML loop
        'tasks_json': json.dumps(tasks_data, cls=DjangoJSONEncoder)  # pass JSON for JavaScript
    })

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def create_task_view(request):
    skills = Skill.objects.all()
    if request.method == 'POST':
        # Required fields
        title       = request.POST.get('title')
        description = request.POST.get('description')
        location    = request.POST.get('location')
        lat         = float(request.POST.get('latitude'))
        lng         = float(request.POST.get('longitude'))
        payment     = request.POST.get('payment')
        duration    = int(request.POST.get('duration_in_minutes') or 0)
        # Parse datetime-local value, e.g. "2025-04-28T14:30"
        fmt = '%Y-%m-%dT%H:%M'
        available_from = timezone.make_aware(
            datetime.strptime(request.POST.get('available_from'), fmt),
            timezone.get_current_timezone()
        )
        available_to   = timezone.make_aware(
            datetime.strptime(request.POST.get('available_to'), fmt),
            timezone.get_current_timezone()
        )
        # Create task
        task = Task.objects.create(
            title=title,
            description=description,
            status='available',
            latitude=lat,
            longitude=lng,
            location=location,
            available_from=available_from,
            available_to=available_to,
            payment=payment,
            duration_in_minutes=duration,
            creator=request.user
        )
        # Attach skills (could be empty for "no skill")
        selected = request.POST.getlist('skills')
        if selected:
            task.skills.set(selected)
        return redirect('task_detail', task_id=task.id)

    return render(request, 'create_task.html', {
        'skills': skills
    })


@login_required
def apply_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    TaskApplication.objects.get_or_create(task=task, user=request.user)
    
    # Redirect to the task detail page
    return redirect('task_detail', task_id=task.id)

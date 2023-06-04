import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from . import models
from .forms import NewUserForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .models import *
from .forms import *

# Create your views here.

@login_required
def home(request):
    sendemail()
    form = TaskForm()

    return render(request, 'index.html', {'form': form})

@login_required
def add_task(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST['title']
        due_date = request.POST['due_date']
        description = request.POST['description']

        task = Schedule(title=title, due_date=due_date,
                        description=description, user=user)
        task.save()
        return redirect('task_list')
    else:
        return render(request, 'index.html')

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'index.html', {'form': form})

@login_required
def task_list(request):
    user = request.user
    tasks = Schedule.objects.all()
    details = user.username
    return render(request, 'task_list.html', {'tasks': tasks, 'credentails': details})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

@login_required
def updateList(request, pk):
    task = Schedule.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect("home")
    context = {'form': form}

    return render(request, 'update_task.html', context)

@login_required
def deleteTask(request, pk):
    item = Schedule.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('home')

    context = {'item': item}
    return render(request, 'delete_task.html', context)

def sendemail(request):
    emails = []
    for n in Schedule.objects.all():
       if n.due_date.replace(tzinfo=None) >= datetime.datetime.now():
             for k in User.objects.all():
                 emails.append(k.email)
                 email_subject = 'Task Reminder'
                 message2 = render_to_string("email.html", {
                            'name': k.username,
                        })
                 email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    emails,
                )
                 email.fail_silently = False
                 email.send()

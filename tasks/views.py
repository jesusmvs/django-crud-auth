from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request ,"home.html")

def signup(request):
    if request.method == 'GET':
        return render(request ,"signup.html", {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Register User
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                #print("Error")
                return render(request ,"signup.html", {
                    "form": UserCreationForm,
                    "error": 'User already exist'
                })
        else:
            print("pw")
            return render(request ,"signup.html", {
                "form": UserCreationForm,
                "error": 'Password doesn\'t match'
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user_id=request.user.id, dateCompleted__isnull=True)
    return render(request ,"tasks/tasks.html", {
        "tasks":tasks,
        "title": "Pending"
    })

@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request ,"tasks/tasks.html", {
        "tasks":tasks,
        "title": "Completed"
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            "form": TaskForm
        })
    else:
        #print(request.POST)
        try:
            form = TaskForm(request.POST)
            # commit false to just see the result
            new_task = form.save(commit=False)
            #we add the user instance because it has a relationship
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
            #task = Task.objects.create(title=request.POST['title'],description=request.POST['description'],important=request.POST['important'],user_id=request.POST['title'])
        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm,
                "error": "Invalid Data"
            })

@login_required
def task_detail(request,id):
    if request.method == 'GET':
        #task = Task.objects.get(id=id) # or pk=id
        task = get_object_or_404(Task, pk=id, user_id=request.user.id)
        form = TaskForm(instance=task)
        return render(request, 'tasks/detail.html', {
            "task": task,
            "form": form
        })
    else:
        try:
            #task = Task.objects.get(id=id) # or pk=id
            task = get_object_or_404(Task, pk=id, user_id=request.user.id)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/detail.html', {
                "task": task,
                "form": form,
                "error": "Error updating!"
            })

@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks') 

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                "form": AuthenticationForm,
                "error": 'wrong credentials!'
            })
        else:
            login(request,user)
            return redirect('tasks')


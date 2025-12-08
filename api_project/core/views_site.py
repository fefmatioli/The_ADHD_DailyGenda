from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Note, Task, Event
from .forms import NoteForm, TaskForm, EventForm, CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout


@login_required
def dashboard(request):
    today = date.today()
    todays_events = Event.objects.filter(user=request.user, date=today).order_by('time')
    month_events = Event.objects.filter(
        user=request.user, 
        date__month=today.month,
        date__year=today.year
    ).exclude(date=today).order_by('date')
    future_events = Event.objects.filter(user=request.user, date__gt=today).exclude(date__month=today.month).order_by('date')
    
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    tasks = Task.objects.filter(user=request.user).order_by('done', '-created_at')

    context = {
        "today": today,
        "todays_events": todays_events,
        "month_events": month_events,
        "future_events": future_events,
        "notes": notes,
        "tasks": tasks,
        "note_form": NoteForm(),
        "task_form": TaskForm(),
        "event_form": EventForm(),
    }
    return render(request, "dashboard.html", context)

@login_required
def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
    return redirect("dashboard")

@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
    return redirect("dashboard")

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
    return redirect("dashboard")

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.done = not task.done
    task.save()
    return redirect("dashboard")

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect("dashboard")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("dashboard")

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    event.delete()
    return redirect("dashboard")

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, "note_detail.html", {"note": note})

@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = NoteForm(instance=note)
    return render(request, "note_edit.html", {"form": form, "note": note})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    return render(request, "event_detail.html", {"event": event})

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = EventForm(instance=event)
    return render(request, "event_edit.html", {"form": form, "event": event})

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def user_logout(request):
    logout(request)             
    return redirect("login") 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Note, Task, Event
from .forms import NoteForm, TaskForm, EventForm, CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
import calendar
from datetime import date
from django.utils import timezone
from .models import Event

@login_required
def dashboard(request):
    today = date.today()
    
    todays_events = Event.objects.filter(user=request.user, date=today).order_by('time')
    month_events = Event.objects.filter(
        user=request.user, 
        date__month=today.month,
        date__year=today.year
    ).exclude(date=today).order_by('date')
    
    notes = Note.objects.filter(user=request.user).order_by('-id') 
    tasks = Task.objects.filter(user=request.user).order_by('done', '-id')

    context = {
        "today": today,
        "todays_events": todays_events,
        "month_events": month_events,
        "notes": notes,
        "tasks": tasks,
        "note_form": NoteForm(),
        "task_form": TaskForm(),
        "event_form": EventForm(),
    }

    context.update(build_calendar_context(request.user))

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

def build_calendar_context(user, year=None, month=None):
    today = timezone.localdate()

    year = int(year) if year is not None else today.year
    month = int(month) if month is not None else today.month

    cal = calendar.Calendar(firstweekday=6)  # Sunday
    month_days = list(cal.itermonthdates(year, month))
    weeks_dates = [month_days[i:i+7] for i in range(0, len(month_days), 7)]

    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    month_events = (
        Event.objects
        .filter(user=user, date__range=(first_day, last_day))
        .order_by("date", "time")
    )

    events_by_day = {}
    for ev in month_events:
        events_by_day.setdefault(ev.date, []).append(ev)

    weeks = []
    for week in weeks_dates:
        week_cells = []
        for day in week:
            week_cells.append({
                "day": day,
                "is_out": day.month != month,
                "is_today": day == today,
                "events": events_by_day.get(day, []),
            })
        weeks.append(week_cells)

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    return {
        "cal_year": year,
        "cal_month": month,
        "cal_month_name": calendar.month_name[month],
        "cal_weeks": weeks,
        "cal_today": today,
        "cal_prev_year": prev_year,
        "cal_prev_month": prev_month,
        "cal_next_year": next_year,
        "cal_next_month": next_month,
        "cal_month_events": month_events,
    }

@login_required
def calendar_month(request, year=None, month=None):
    ctx = build_calendar_context(request.user, year=year, month=month)
    return render(request, "calendar_page.html", ctx)

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
from django import forms
from .models import Note, Task, Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "category"]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "time", "end_time", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]
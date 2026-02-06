from django.contrib import admin
from .models import Note, Event, Task

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "user", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "content", "user__username")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "time", "end_time", "user", "created_at")
    list_filter = ("date", "created_at")
    search_fields = ("title", "description", "user__username")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "done", "user", "created_at")
    list_filter = ("done", "created_at")
    search_fields = ("title", "user__username")
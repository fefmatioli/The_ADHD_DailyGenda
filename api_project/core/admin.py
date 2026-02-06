from django.contrib import admin
from .models import Note, Event, Task

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "date", "user")
    list_filter = ("category", "date")
    search_fields = ("title", "content", "user__username")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "time", "end_time", "user")
    list_filter = ("date",)
    search_fields = ("title", "description", "user__username")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "done", "user")
    list_filter = ("done",)
    search_fields = ("title", "user__username")
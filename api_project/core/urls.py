from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_site

urlpatterns = [
    path("", views_site.dashboard, name="dashboard"), #
    path("create-note/", views_site.create_note, name="create_note"),
    path("create-task/", views_site.create_task, name="create_task"),
    path("create-event/", views_site.create_event, name="create_event"),
    path("toggle-task/<int:task_id>/", views_site.toggle_task, name="toggle_task"),
    path("delete-note/<int:note_id>/", views_site.delete_note, name="delete_note"),
    path("delete-task/<int:task_id>/", views_site.delete_task, name="delete_task"),
    path("delete-event/<int:event_id>/", views_site.delete_event, name="delete_event"),
    path("note/<int:note_id>/", views_site.note_detail, name="note_detail"),
    path("event/<int:event_id>/", views_site.event_detail, name="event_detail"),
    path("event/<int:event_id>/edit/", views_site.event_edit, name="event_edit"),
    path("note/<int:note_id>/edit/", views_site.note_edit, name="note_edit"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"), 
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 
    path("signup/", views_site.signup, name="signup"), 
    path("calendar/", views_site.calendar_month, name="calendar_month"),
    path("calendar/<int:year>/<int:month>/", views_site.calendar_month, name="calendar_month"),
]

from rest_framework import viewsets, permissions
from django.utils.dateparse import parse_date
from .models import Note, Event, Task
from .serializers import NoteSerializer, EventSerializer, TaskSerializer


class OwnerQuerysetMixin:
    """
    Garante que cada usuário só enxerga e manipula os próprios registros.
    """
    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        return self.apply_filters(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def apply_filters(self, qs):
        return qs


class NoteViewSet(OwnerQuerysetMixin, viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def apply_filters(self, qs):
        date_str = self.request.query_params.get("date")
        category = self.request.query_params.get("category")
        done = self.request.query_params.get("done")

        if date_str:
            date = parse_date(date_str)
            if date:
                qs = qs.filter(date=date)

        if category:
            qs = qs.filter(category=category)

        if done is not None:
            if done.lower() in ("1", "true", "t", "yes", "y"):
                qs = qs.filter(done=True)
            elif done.lower() in ("0", "false", "f", "no", "n"):
                qs = qs.filter(done=False)
        return qs


class EventViewSet(OwnerQuerysetMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def apply_filters(self, qs):
        date_str = self.request.query_params.get("date")
        if date_str:
            date = parse_date(date_str)
            if date:
                qs = qs.filter(date=date)
        return qs


class TaskViewSet(OwnerQuerysetMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def apply_filters(self, qs):
        done = self.request.query_params.get("done")
        if done is not None:
            if done.lower() in ("1", "true", "t", "yes", "y"):
                qs = qs.filter(done=True)
            elif done.lower() in ("0", "false", "f", "no", "n"):
                qs = qs.filter(done=False)
        return qs
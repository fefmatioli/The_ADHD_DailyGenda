from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework.routers import DefaultRouter
from core.views import NoteViewSet, EventViewSet, TaskViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'events', EventViewSet, basename='event')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)), 
    path('dashboard/', include('core.urls')), #hmtl
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)), #API
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

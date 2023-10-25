"""
URL mappings for the truck app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from trucks import views


router = DefaultRouter()
router.register('trucks', views.TruckViewSet)
router.register('maintenancelogs', views.MaintenanceLogViewSet)

app_name = 'trucks'

urlpatterns = [
    path('', include(router.urls))
]

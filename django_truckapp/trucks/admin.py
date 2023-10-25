"""
Django admin customization
"""
# Django imports
from django.contrib import admin
# Custom imports
from trucks.models import Truck, MaintenanceLog


class MaintenanceLogAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'log_number',
    )
    ordering = ('-date', )


class TruckAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )
    list_display = (
        'licence_plate',
        'make',
        'model',
        'year',
        'vin',
        'color',
        'engine',
        'fuel',
        'transmission',
        'body_style',
        'user',
    )
    ordering = ('licence_plate', )

    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated:
            user = request.user
            obj.user = user
            obj.save()


admin.site.register(Truck, TruckAdmin)
admin.site.register(MaintenanceLog, MaintenanceLogAdmin)

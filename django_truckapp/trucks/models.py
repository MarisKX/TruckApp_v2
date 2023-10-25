"""
Database truck models.
"""
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Truck(models.Model):
    """Truck Objects"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Last Edit By',
        on_delete=models.PROTECT)
    licence_plate = models.CharField(max_length=12)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ])
    vin = models.CharField(max_length=17, unique=True)

    color = models.CharField(max_length=30, blank=True, null=True)
    engine = models.CharField(max_length=30, blank=True, null=True)
    fuel = models.CharField(max_length=30, blank=True, null=True)
    transmission = models.CharField(max_length=60, blank=True, null=True)
    body_style = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.licence_plate


class MaintenanceLog(models.Model):
    """Maintenance Logs Objects"""
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    log_number = models.CharField(max_length=8, default='1')
    date = models.DateField(auto_now=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Created By',
        on_delete=models.PROTECT,
        default=1)

    def __str__(self):
        return self.log_number

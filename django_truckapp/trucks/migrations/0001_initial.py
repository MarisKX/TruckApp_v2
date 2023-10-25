# Generated by Django 4.2.6 on 2023-10-25 14:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_plate', models.CharField(max_length=12)),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
                ('vin', models.CharField(max_length=17, unique=True)),
                ('color', models.CharField(blank=True, max_length=30, null=True)),
                ('engine', models.CharField(blank=True, max_length=30, null=True)),
                ('fuel', models.CharField(blank=True, max_length=30, null=True)),
                ('transmission', models.CharField(blank=True, max_length=60, null=True)),
                ('body_style', models.CharField(blank=True, max_length=60, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Last Edit By')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_number', models.CharField(default='1', max_length=8)),
                ('date', models.DateField()),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trucks.truck')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
        ),
    ]
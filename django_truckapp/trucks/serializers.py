"""
Serializers for the trucks API View
"""
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from trucks.models import Truck, MaintenanceLog


class TruckSerializer(serializers.ModelSerializer):
    """Serializer for trucks"""

    year = serializers.IntegerField(validators=[
        MinValueValidator(1900),
        MaxValueValidator(datetime.now().year)
    ])

    class Meta:
        model = Truck
        fields = [
            'id',
            'user',
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
        ]
        read_only_fields = ['id', 'user', ]

    def validate_year(self, value):
        """
        Check that the year is between 1900 and the current year.
        """
        current_year = datetime.now().year
        if value < 1900 or value > current_year:
            raise serializers.ValidationError(
                f'Year must be between 1900 and {current_year}'
            )
        return value


class TruckDetailSerializer(TruckSerializer):
    """Serializer for recipe detail view"""

    class Meta(TruckSerializer.Meta):
        fields = TruckSerializer.Meta.fields + ['color', 'engine', ]


class MaintenanceLogSerializer(serializers.ModelSerializer):
    """Serializer for maintenance logs"""

    class Meta:
        model = MaintenanceLog
        fields = [
            'id',
            'truck',
            'log_number',
            'date',
            'user',
        ]
        read_only_fields = ['truck', 'user', ]

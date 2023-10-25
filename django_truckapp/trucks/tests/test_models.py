"""
Tests for models.
"""
from decimal import Decimal  # noqa
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from trucks.models import Truck


def create_user(email='user@example.com', password='Pass1234'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_truck(self):
        """Test creating a truck is successfull"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        truck = Truck.objects.create(
            user=user,
            licence_plate="AH6814",
            make="FREIGHTLINER",
            model="CASCADIA 125",
            year="2016",
            vin="3AKJGLD58GSHR6402"
        )

        self.assertEqual(str(truck), truck.licence_plate)

    def test_create_truck_with_duplicate_vin(self):
        """Test creating a truck with a duplicate VIN fails"""
        user = get_user_model().objects.create_user(
            'test2@example.com',
            'testpass123',
        )
        Truck.objects.create(
            user=user,
            licence_plate="AH6814",
            make="FREIGHTLINER",
            model="CASCADIA 125",
            year=2016,
            vin="3AKJGLD58GSHR6402"
        )
        with self.assertRaises(IntegrityError):
            Truck.objects.create(
                user=user,
                licence_plate="NEW_PLATE",
                make="FREIGHTLINER",
                model="CASCADIA 125",
                year=2017,
                vin="3AKJGLD58GSHR6402"
            )

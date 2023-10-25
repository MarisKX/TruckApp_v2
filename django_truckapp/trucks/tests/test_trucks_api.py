
"""
Tests for Trucks APis
"""
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from trucks.models import Truck
from trucks.serializers import (
    TruckSerializer,
    TruckDetailSerializer,
)


TRUCKS_URL = reverse('trucks:truck-list')


def detail_url(truck_id):
    """Create and return a truck detail URL"""
    return reverse('trucks:truck-detail', args=[truck_id])


def create_truck(user, **params):
    """Create and return a sample truck"""
    defaults = {
        'licence_plate': "AH6814",
        'make': "FREIGHTLINER",
        'model': "CASCADIA 125",
        'year': "2016",
    }
    defaults.update(params)

    truck = Truck.objects.create(user=user, **defaults)
    return truck


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicTruckApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(TRUCKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTruckApiTests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass1235')
        self.client.force_authenticate(self.user)

    def test_retrieve_trucks(self):
        """Test retrieving a list of trucks"""
        create_truck(
            user=self.user,
            vin="3AKJGLD58GSHR6402"
        )
        create_truck(
            user=self.user,
            vin="3AKJGLD58GSHR6403"
        )

        res = self.client.get(TRUCKS_URL)

        trucks = Truck.objects.all().order_by('id')
        serializer = TruckSerializer(trucks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_truck_detail(self):
        """Test get truck detail"""
        truck = create_truck(
            user=self.user,
            vin="3AKJGLD58GSHR6402"
        )

        url = detail_url(truck.id)
        res = self.client.get(url)

        serializer = TruckDetailSerializer(truck)
        self.assertEqual(res.data, serializer.data)

    def test_create_truck(self):
        """Test creating a truck via API"""
        payload = {
            'licence_plate': "AH6814",
            'make': "FREIGHTLINER",
            'model': "CASCADIA 125",
            'year': 2016,
            'vin': "3AKJGLD58GSHR6402",
            'color': 'White',
            'engine': "14.8L 6"
        }
        res = self.client.post(TRUCKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        truck = Truck.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(truck, k), v)
        self.assertEqual(truck.user, self.user)

    def test_update_truck_last_edited_by(self):
        """Test updating a truck's via API"""
        truck = Truck.objects.create(
            user=self.user,
            licence_plate="AH6814",
            make="FREIGHTLINER",
            model="CASCADIA 125",
            year=2016,
            vin="3AKJGLD58GSHR6402"
        )
        original_make = truck.make

        user2 = create_user(
            email='test2@example.com',
            password='testpass456'
        )

        self.client.force_authenticate(user=user2)

        payload = {'licence_plate': "JR6517", 'engine': "15.2L 8"}
        url = detail_url(truck.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        truck.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(getattr(truck, k), v)

        self.assertEqual(truck.user, user2)
        self.assertEqual(truck.make, original_make)

    def test_update_user_returns_error(self):
        """Test chaning the user results in an error"""
        new_user = create_user(email='test@example.com', password='123456Test')
        truck = create_truck(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(truck.id)
        self.client.patch(url, payload)

        truck.refresh_from_db()
        self.assertEqual(truck.user, self.user)

    def test_delete_truck(self):
        """Test deleting a truck successfull"""
        truck = create_truck(user=self.user)

        url = detail_url(truck.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Truck.objects.filter(id=truck.id).exists())

    def test_create_truck_valid_year(self):
        """Test creating a truck with a valid year"""
        payload = {
            'licence_plate': "VALID1",
            'make': "VALID_MAKE",
            'model': "VALID_MODEL",
            'year': datetime.now().year,
            'vin': "VALID_VIN1",
        }
        res = self.client.post(TRUCKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        truck = Truck.objects.get(id=res.data['id'])
        self.assertEqual(truck.year, payload['year'])

    def test_create_truck_invalid_year(self):
        """Test creating a truck with an invalid year should fail"""
        payload = {
            'licence_plate': "INVALID1",
            'make': "INVALID_MAKE",
            'model': "INVALID_MODEL",
            'year': 1800,  # Invalid year
            'vin': "INVALID_VIN1",
        }
        res = self.client.post(TRUCKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_truck_invalid_year(self):
        """Test updating a truck with an invalid year should fail"""
        truck = create_truck(
            user=self.user,
            vin="VALID_VIN2"
        )
        payload = {'year': 1800}  # Invalid year
        url = detail_url(truck.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        truck.refresh_from_db()
        self.assertNotEqual(truck.year, 1800)

"""
Views for the trucks API's
"""
from rest_framework import (
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from trucks.models import (
    Truck,
    MaintenanceLog,
)
from trucks import serializers


class TruckViewSet(viewsets.ModelViewSet):
    """View for manage trucks API's"""
    serializer_class = serializers.TruckDetailSerializer
    queryset = Truck.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.TruckSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    """View for manage maintenance logs API's"""
    serializer_class = serializers.MaintenanceLogSerializer
    queryset = MaintenanceLog.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.MaintenanceLogSerializer

        return self.serializer_class

    def get_queryset(self):
        queryset = MaintenanceLog.objects.all()

        truck_id = self.request.query_params.get('truck_id')
        print(truck_id)
        if truck_id is not None:
            # If truck_id is provided in the URL,
            # filter maintenance logs by truck
            queryset = queryset.filter(truck=truck_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

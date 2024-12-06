from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.decorators import validate_request
from services.serializers.service_serializer import ServiceSerializer, ServiceUpdateSerializer
from services.service_models.service import Service


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()  # Add this to resolve the basename issue
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ServiceUpdateSerializer if self.action in ['update', 'partial_update'] else ServiceSerializer

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id', None)
        if provider_id:
            return Service.objects.filter(provider_id=provider_id)
        return Service.objects.all()

    @validate_request(ServiceSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @validate_request(ServiceUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @validate_request(ServiceUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Service deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)


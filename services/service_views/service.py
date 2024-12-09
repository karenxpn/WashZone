from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from WashZone.permissions import IsOwner
from authentication.decorators import validate_request
from services.serializers.service_serializer import ServiceSerializer, ServiceUpdateSerializer
from services.service_models.service import Service
from services.service_views.add_feature_to_service import add_feature_to_service
from services.service_views.remove_feature_from_service import remove_feature
from services.service_views.update_linked_feature import update_feature


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ServiceUpdateSerializer if self.action in ['update', 'partial_update'] else ServiceSerializer

    def get_permissions(self):
        return [IsOwner()] if self.action in ['update', 'partial_update', 'destroy'] else super().get_permissions()

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id', None)
        if provider_id:
            return Service.objects.filter(provider_id=provider_id).prefetch_related('features__feature')
        return Service.objects.prefetch_related('features__feature')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-feature')
    def add_feature(self, request, pk=None):
        return add_feature_to_service(self, request)

    @action(detail=True, methods=['delete'], url_path='remove-feature')
    def remove_feature(self, request, pk=None):
        return remove_feature(self, request)

    @action(detail=True, methods=['patch'], url_path='update-feature')
    def update_feature(self, request, pk=None):
        return update_feature(self, request, pk)


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


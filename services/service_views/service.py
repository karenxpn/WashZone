from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from WashZone.permissions import IsOwner
from authentication.decorators import validate_request
from services.schemas.service_schemas import service_schemas, additional_features_list_schema, add_feature_schema, \
    remove_feature_schema, update_feature_schema
from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.serializers.service_serializer import ServiceSerializer, ServiceUpdateSerializer, ServiceListSerializer, \
    CreateServiceSerializer
from services.service_models.feature import ServiceFeature
from services.service_models.service import Service
from services.service_views.add_feature_to_service import add_feature_to_service
from services.service_views.remove_feature_from_service import remove_feature
from services.service_views.update_linked_feature import update_feature


@service_schemas
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        if self.action == 'create':
            return CreateServiceSerializer

        return ServiceUpdateSerializer if self.action in ['update', 'partial_update'] else ServiceSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsOwner(), IsAdminUser()] if self.action in ['create', 'update', 'partial_update', 'destroy'] else super().get_permissions()


    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id', None)

        if self.action == 'retrieve':
            feature_queryset = ServiceFeature.objects.filter(is_included=True).select_related('feature')
            queryset = Service.objects.prefetch_related(Prefetch('features', queryset=feature_queryset))
        else:
            queryset = Service.objects.all()

        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @additional_features_list_schema
    @action(detail=True, methods=['get'], url_path='additional-features')
    def additional_features(self, request, pk=None):
        try:
            service = self.get_object()
            excluded_features = service.features.filter(is_included=False).select_related('feature')
            serializer = ServiceFeatureSerializer(excluded_features, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

    @add_feature_schema
    @action(detail=True, methods=['post'], url_path='add-feature')
    def add_feature(self, request, pk=None):
        return add_feature_to_service(self, request)

    @remove_feature_schema
    @action(detail=True, methods=['delete'], url_path='remove-feature/(?P<feature_id>\d+)')
    def remove_feature(self, request, pk=None, feature_id=None):
        return remove_feature(self, request, pk, feature_id)

    @update_feature_schema
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


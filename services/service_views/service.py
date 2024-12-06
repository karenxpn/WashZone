from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.decorators import validate_request
from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.serializers.service_serializer import ServiceSerializer, ServiceUpdateSerializer
from services.service_models.feature import Feature, ServiceFeature
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


    @action(detail=True, methods=['post'], url_path='add-feature')
    def add_feature(self, request, pk=None):
        service = self.get_object()
        feature_id = request.data.get('feature_id')
        is_included = request.data.get('is_included', False)
        extra_cost = request.data.get('extra_cost', 0)

        if not feature_id:
            return Response({"error": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the feature exists
            feature = Feature.objects.get(pk=feature_id)

            # Create or update the ServiceFeature
            service_feature, created = ServiceFeature.objects.get_or_create(
                service=service,
                feature=feature,
                defaults={'is_included': is_included, 'extra_cost': extra_cost}
            )

            # If not created, update the existing entry
            if not created:
                service_feature.is_included = is_included
                service_feature.extra_cost = extra_cost
                service_feature.save()

            serializer = ServiceFeatureSerializer(service_feature)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except Feature.DoesNotExist:
            return Response({"error": "Feature not found."}, status=status.HTTP_404_NOT_FOUND)



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


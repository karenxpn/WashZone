from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.decorators import validate_request
from services.serializers.feature_serializer import FeatureSerializer, FeatureUpdateSerializer
from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.service_models.feature import Feature, ServiceFeature


class FeatureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Feature.objects.all()

    def get_serializer_class(self):
        return FeatureUpdateSerializer if self.action in ['update', 'partial_update'] else FeatureSerializer

    @validate_request(FeatureSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @validate_request(FeatureUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return update_feature(self, request, *args, **kwargs)

    @validate_request(FeatureUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        return update_feature(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Feature deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Feature not found"}, status=status.HTTP_404_NOT_FOUND)


def update_feature(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    feature = serializer.save()

    # Propagate changes to related ServiceFeature records
    related_service_features = ServiceFeature.objects.filter(feature=feature)
    for service_feature in related_service_features:
        # Use the ServiceFeatureSerializer to validate and save changes
        service_feature_data = {
            'service': service_feature.service.id,
            'feature': service_feature.feature.id,
            'is_included': service_feature.is_included,
            'extra_cost': feature.cost,
        }
        sf_serializer = ServiceFeatureSerializer(service_feature, data=service_feature_data, partial=True)
        if sf_serializer.is_valid(raise_exception=True):
            sf_serializer.save()

    return Response(serializer.data)



from rest_framework import status
from rest_framework.response import Response

from assistant.vector_helper import update_service_in_provider_embedding
from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.serializers.service_serializer import ServiceSerializer
from services.service_models.feature import Feature, ServiceFeature

from rest_framework.exceptions import PermissionDenied

def validate_ownership(user, service=None, feature=None, service_feature=None):
    if service and service.owner != user:
        raise PermissionDenied("You do not own this service.")
    if feature and feature.owner != user:
        raise PermissionDenied("You do not own this feature.")
    if service_feature and service_feature.owner != user:
        raise PermissionDenied("You do not own this service feature.")


def add_feature_to_service(self, request,  pk=None, feature_id=None):
    service = self.get_object()
    is_included = request.data.get('is_included', False)
    extra_cost = request.data.get('extra_cost', None)
    extra_time_in_minutes = request.data.get('extra_time_in_minutes', 0)

    if not feature_id:
        return Response({"message": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        feature = Feature.objects.get(pk=feature_id)

        if extra_cost is None and not is_included:
            extra_cost = feature.cost
        elif is_included:
            extra_cost = 0

        service_feature = ServiceFeature.objects.filter(service=service, feature=feature).first()
        validate_ownership(user=request.user, service=service, feature=feature, service_feature=service_feature)

        service_feature, created = ServiceFeature.objects.update_or_create(
            owner=request.user,
            service=service,
            feature=feature,
            defaults={'is_included': is_included, 'extra_cost': extra_cost, 'extra_time_in_minutes': extra_time_in_minutes}
        )

        serializer = ServiceFeatureSerializer(service_feature)
        update_service_in_provider_embedding(service.provider, service, ServiceSerializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    except Feature.DoesNotExist:
        return Response({"message": "Feature not found."}, status=status.HTTP_404_NOT_FOUND)

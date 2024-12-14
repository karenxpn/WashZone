from rest_framework import status
from rest_framework.response import Response

from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.service_models.feature import ServiceFeature, Feature
from services.service_views.add_feature_to_service import validate_ownership


def update_feature(self, request, pk=None):
    service = self.get_object()
    feature_id = request.data.get('feature_id')
    is_included = request.data.get('is_included')
    extra_cost = request.data.get('extra_cost')
    extra_time_in_minutes = request.data.get('extra_time_in_minutes', 0)

    if not feature_id:
        return Response({"message": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Ensure the feature is linked to the service
        feature = Feature.objects.get(pk=feature_id)
        service_feature = ServiceFeature.objects.filter(service=service, feature=feature).first()
        validate_ownership(user=request.user, service=service, feature=feature, service_feature=service_feature)

        service_feature = ServiceFeature.objects.get(service=service, feature_id=feature_id)

        # Update fields if provided in the request
        if is_included is not None:
            service_feature.is_included = is_included

        if extra_cost is not None:
            service_feature.extra_cost = extra_cost

        if extra_time_in_minutes is not None:
            service_feature.extra_time_in_minutes = extra_time_in_minutes

        if is_included:
            service_feature.extra_cost = 0


        service_feature.save()  # Save the changes

        serializer = ServiceFeatureSerializer(service_feature)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ServiceFeature.DoesNotExist:
        return Response({"message": "The feature is not linked to this service."}, status=status.HTTP_404_NOT_FOUND)
    except Feature.DoesNotExist:
        return Response({'message': 'The feature is not found.'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import status
from rest_framework.response import Response

from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.service_models.feature import ServiceFeature


def update_feature(self, request, pk=None):
    service = self.get_object()
    feature_id = request.data.get('feature_id')
    is_included = request.data.get('is_included')
    extra_cost = request.data.get('extra_cost')

    if not feature_id:
        return Response({"message": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Ensure the feature is linked to the service
        service_feature = ServiceFeature.objects.get(service=service, feature_id=feature_id)

        # Update fields if provided in the request
        if is_included is not None:
            service_feature.is_included = is_included

        if extra_cost is not None:
            service_feature.extra_cost = extra_cost

        service_feature.save()  # Save the changes

        serializer = ServiceFeatureSerializer(service_feature)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ServiceFeature.DoesNotExist:
        return Response({"message": "The feature is not linked to this service."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import status
from rest_framework.response import Response

from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.service_models.feature import Feature, ServiceFeature

def add_feature_to_service(self, request):
    service = self.get_object()
    feature_id = request.data.get('feature_id')
    is_included = request.data.get('is_included', False)
    extra_cost = request.data.get('extra_cost', 0)

    if not feature_id:
        return Response({"message": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        feature = Feature.objects.get(pk=feature_id)

        # Use update_or_create to handle both creation and updating in one step
        service_feature, created = ServiceFeature.objects.update_or_create(
            service=service,
            feature=feature,
            defaults={'is_included': is_included, 'extra_cost': extra_cost}
        )

        serializer = ServiceFeatureSerializer(service_feature)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    except Feature.DoesNotExist:
        return Response({"message": "Feature not found."}, status=status.HTTP_404_NOT_FOUND)
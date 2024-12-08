from rest_framework import status
from rest_framework.response import Response
from services.service_models.feature import ServiceFeature

def remove_feature(self, request, pk=None):
    service = self.get_object()
    feature_id = request.data.get('feature_id')

    if not feature_id:
        return Response({"message": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Ensure the feature is linked to the service
        service_feature = ServiceFeature.objects.get(service=service, feature_id=feature_id)
        service_feature.delete()  # Delete the relationship
        return Response({"message": "Feature removed from service successfully."}, status=status.HTTP_200_OK)

    except ServiceFeature.DoesNotExist:
        return Response({"message": "The feature is not linked to this service."}, status=status.HTTP_404_NOT_FOUND)

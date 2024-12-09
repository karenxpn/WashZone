from rest_framework import status
from rest_framework.response import Response
from services.service_models.feature import ServiceFeature, Feature
from services.service_views.add_feature_to_service import validate_ownership


def remove_feature(self, request, pk=None):
    service = self.get_object()
    feature_id = request.data.get('feature_id')

    if not feature_id:
        return Response({"message": "Feature ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Ensure the feature is linked to the service
        feature = Feature.objects.get(pk=feature_id)
        service_feature = ServiceFeature.objects.filter(service=service, feature=feature).first()
        validate_ownership(user=request.user, service=service, feature=feature, service_feature=service_feature)

        service_feature = ServiceFeature.objects.get(service=service, feature_id=feature_id)
        service_feature.delete()  # Delete the relationship
        return Response({"message": "Feature removed from service successfully."}, status=status.HTTP_200_OK)

    except ServiceFeature.DoesNotExist:
        return Response({"message": "The feature is not linked to this service."}, status=status.HTTP_404_NOT_FOUND)
    except Feature.DoesNotExist:
        return Response({'message': 'The feature is not found.'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.decorators import validate_request
from services.serializers.feature_serializer import FeatureSerializer, FeatureUpdateSerializer
from services.service_models.feature import Feature


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
        return super().update(request, *args, **kwargs)

    @validate_request(FeatureUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Feature deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Feature not found"}, status=status.HTTP_404_NOT_FOUND)
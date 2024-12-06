from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.decorators import validate_request
from services.serializers.provider_serializer import ProviderUpdateSerializer, ProviderSerializer
from services.service_models.provider import Provider


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ProviderUpdateSerializer if self.action in ['update', 'partial_update'] else ProviderSerializer


    @validate_request(ProviderSerializer)
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                return Response({"message": "A provider with this information already exists."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @validate_request(ProviderUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @validate_request(ProviderUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Provider deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Provider not found"}, status=status.HTTP_404_NOT_FOUND)

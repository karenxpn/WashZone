from django.contrib.gis.db.models.functions import Distance
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from WashZone.permissions import IsOwner
from WashZone.presigned_url import generate_presigned_url
from authentication.decorators import validate_request
from services.schemas.providers_schemas import providers_schema
from services.serializers.provider_serializer import (ProviderUpdateSerializer,
                                                      ProviderSerializer, \
    CreateProviderSerializer)
from services.service_models.provider import Provider
from user.schemas import presigned_url_schema


@providers_schema
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProviderSerializer
        return ProviderUpdateSerializer if self.action in ['update', 'partial_update'] else ProviderSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsOwner(), IsAdminUser()] if self.action in ['create', 'update', 'partial_update', 'destroy'] else super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.location:
            return Provider.objects.annotate(distance=Distance('location', user.location)).order_by('distance')
        return Provider.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @validate_request(CreateProviderSerializer)
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            print(e)
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

    @presigned_url_schema
    @action(detail=False, methods=['post'], url_path='presigned-url', permission_classes=[IsAuthenticated, IsAdminUser])
    def presigned_url(self, request):
        file_name = request.data.get('file_name')
        file_type = request.data.get('file_type')

        return generate_presigned_url(file_name, file_type, 'providers')

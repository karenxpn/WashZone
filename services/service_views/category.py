from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from WashZone.permissions import IsSuperAdmin
from authentication.decorators import validate_request
from services.serializers.category_serializer import CategorySerializer, CategoryUpdateSerializer
from services.serializers.provider_serializer import ProviderSerializer
from services.service_models.category import Category
from services.schemas.category_schemas import category_schema, category_provider_schema


@category_schema
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    def get_serializer_class(self):
        return CategoryUpdateSerializer if self.action in ['update', 'partial_update'] else CategorySerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsSuperAdmin()] if self.action in ['create', 'update', 'partial_update', 'destroy'] else super().get_permissions()

    @validate_request(CategorySerializer)
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                return Response({"message": "A category with this information already exists."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @category_provider_schema
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def providers(self, request, pk=None):
        try:
            category = self.get_object()
            providers = category.providers.all()
            serializer = ProviderSerializer(providers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    @validate_request(CategoryUpdateSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @validate_request(CategoryUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # Get the object to be deleted
            self.perform_destroy(instance)  # Delete the object
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


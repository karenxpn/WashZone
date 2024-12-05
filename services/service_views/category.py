from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.decorators import validate_request
from services.serializers.category_serializer import CategorySerializer, CategoryUpdateSerializer
from services.service_models.category import Category


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CategorySerializer
        elif self.action in ['update', 'partial_update']:
            return CategoryUpdateSerializer
        return CategorySerializer


    @validate_request(CategorySerializer)
    def create(self, request, *args, **kwargs):
        # The decorator will validate and handle errors for this method
        return super().create(request, *args, **kwargs)

    @validate_request(CategoryUpdateSerializer)
    def update(self, request, *args, **kwargs):
        # Apply the decorator to handle update requests
        return super().update(request, *args, **kwargs)

    @validate_request(CategoryUpdateSerializer)
    def partial_update(self, request, *args, **kwargs):
        # Handles partial updates (PATCH)
        return super().partial_update(request, *args, **kwargs)


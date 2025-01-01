from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from services.serializers.category_serializer import CategorySerializer, CategoryUpdateSerializer
from services.serializers.provider_serializer import ProviderSerializer

category_schema = extend_schema_view(
    list=extend_schema(
        summary="List Categories",
        description="Retrieve a list of all categories.",
        responses={
            200: CategorySerializer(many=True)
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Category",
        description="Retrieve details of a specific category by ID.",
        responses={
            200: CategorySerializer,
        },
    ),
    create=extend_schema(
        summary="Create Category",
        description="Create a new category. Only accessible by super admins.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
        },
    ),
    update=extend_schema(
        summary="Update Category",
        description="Update details of an existing category. Only accessible by super admins.",
        request=CategoryUpdateSerializer,
        responses={
            200: CategoryUpdateSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Category",
        description="Partially update details of an existing category. Only accessible by super admins.",
        request=CategoryUpdateSerializer,
        responses={
            200: CategoryUpdateSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Category",
        description="Delete a category. Only accessible by super admins.",
        responses={
            204: OpenApiResponse(description="Category deleted successfully."),
        },
    ),
)


category_provider_schema = extend_schema(
        summary="List Providers for a Category",
        description="Retrieve all providers associated with a specific category. "
                    "This endpoint returns a list of providers that belong to the specified category.",
        responses={
            200: ProviderSerializer(many=True),
        },
    )
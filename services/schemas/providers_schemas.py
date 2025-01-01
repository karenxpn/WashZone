from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from services.serializers.provider_serializer import ProviderSerializer, CreateProviderSerializer, \
    ProviderUpdateSerializer

providers_schema = extend_schema_view(
    list=extend_schema(
        summary="List Providers",
        description="Retrieve a list of all providers.",
        responses={
            200: ProviderSerializer(many=True)
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Provider",
        description="Retrieve details of a specific provider by ID.",
        responses={
            200: ProviderSerializer,
        },
    ),

    create=extend_schema(
        summary="Create Provider",
        description="Create a new provider. Only accessible by admins.",
        request=CreateProviderSerializer,
        responses={
            201: CreateProviderSerializer,
        },
    ),
    update=extend_schema(
        summary="Update Provider",
        description="Update details of an existing provider. Only accessible by admins.",
        request=ProviderUpdateSerializer,
        responses={
            200: ProviderUpdateSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Provider",
        description="Partially update details of an existing provider. Only accessible by admins.",
        request=ProviderUpdateSerializer,
        responses={
            200: ProviderUpdateSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Provider",
        description="Delete the provider. Only accessible by admins.",
        responses={
            204: OpenApiResponse(description="Category deleted successfully."),
        },
    ),
)
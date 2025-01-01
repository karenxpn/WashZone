from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from services.serializers.feature_serializer import FeatureSerializer, FeatureUpdateSerializer

features_schema = extend_schema_view(
    list=extend_schema(
        summary="List Features",
        description="Retrieve a list of all features.",
        responses={
            200: FeatureSerializer(many=True)
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Feature",
        description="Retrieve details of a specific feature by ID.",
        responses={
            200: FeatureSerializer,
        },
    ),

    create=extend_schema(
        summary="Create Feature",
        description="Create a new feature. Only accessible by admins.",
        request=FeatureSerializer,
        responses={
            201: FeatureSerializer,
        },
    ),
    update=extend_schema(
        summary="Update Feature",
        description="Update details of an existing feature. Only accessible by admins.",
        request=FeatureUpdateSerializer,
        responses={
            200: FeatureUpdateSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Feature",
        description="Partially update details of an existing feature. Only accessible by admins.",
        request=FeatureUpdateSerializer,
        responses={
            200: FeatureUpdateSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Feature",
        description="Delete a feature. Only accessible by admins.",
        responses={
            204: OpenApiResponse(description="Category deleted successfully."),
        },
    ),
)
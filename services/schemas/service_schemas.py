from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter, \
    inline_serializer
from rest_framework import serializers

from services.serializers.service_feature_serializer import ServiceFeatureSerializer
from services.serializers.service_serializer import ServiceListSerializer, ServiceSerializer, CreateServiceSerializer, \
    ServiceUpdateSerializer

service_schemas = extend_schema_view(
    list=extend_schema(
        summary="List Services",
        description="Retrieve a list of all services.",
        responses={
            200: ServiceListSerializer(many=True)
        },
    ),

    retrieve=extend_schema(
        summary="Retrieve Service",
        description="Retrieve details of a specific service by ID.",
        responses={
            200: ServiceSerializer,
        },
    ),

    create=extend_schema(
        summary="Create Service",
        description="Create a new service. Only accessible by admins.",
        request=CreateServiceSerializer,
        responses={
            201: CreateServiceSerializer,
        },
    ),
    update=extend_schema(
        summary="Update Service",
        description="Update details of an existing service. Only accessible by admins.",
        request=ServiceUpdateSerializer,
        responses={
            200: ServiceUpdateSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Service",
        description="Partially update details of an existing service. Only accessible by admins.",
        request=ServiceUpdateSerializer,
        responses={
            200: ServiceUpdateSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Service",
        description="Delete the service. Only accessible by admins.",
        responses={
            204: OpenApiResponse(description="Service deleted successfully."),
        },
    ),
)

additional_features_list_schema = extend_schema(
    summary="Retrieve Additional Features for a Service",
    description=(
        "Retrieve features associated with a specific service that are not included. "
        "This endpoint returns a list of additional features that a service offers."
    ),
    responses={
        200: ServiceFeatureSerializer(many=True),
    },
)

add_feature_schema = extend_schema(
    methods=['POST'],
    summary="Add a Feature to a Service",
    description=(
        "Associate a feature with a specific service. You can specify if the feature is included "
        "and define any additional cost if applicable."
    ),
    request=inline_serializer(
        name='AddFeatureRequest',
        fields={
            'feature_id': serializers.IntegerField(required=True),
            'is_included': serializers.BooleanField(required=False, default=False),
            'extra_cost': serializers.DecimalField(required=False, max_digits=10, decimal_places=2, allow_null=True),
            'extra_time_in_minutes': serializers.DecimalField(required=False, max_digits=10, decimal_places=2, allow_null=True),
        }
    ),
    responses={
        201: ServiceFeatureSerializer,
    },
)

remove_feature_schema = extend_schema(
    summary="Remove a Feature from a Service",
    description=(
        "Remove the association of a feature from a specific service. This action does not delete the feature itself, "
        "only the relationship between the feature and the service."
    ),
    responses={
        200: OpenApiResponse(
            description="Feature removed from service successfully."
        ),
    },
)

update_feature_schema = extend_schema(
    methods=['PATCH'],
    summary="Update a Feature in a Service",
    description=(
        "Update the details of a specific feature linked to a service. "
        "You can modify whether the feature is included, its extra cost, or extra time in minutes."
    ),
    request=inline_serializer(
        name='UpdateFeatureRequest',
        fields={
            'feature_id': serializers.IntegerField(required=True),
            'is_included': serializers.BooleanField(required=False, default=False),
            'extra_cost': serializers.DecimalField(required=False, max_digits=10, decimal_places=2, allow_null=True),
            'extra_time_in_minutes': serializers.DecimalField(required=False, max_digits=10, decimal_places=2, allow_null=True),
        }
    ),
    responses={
        200: ServiceFeatureSerializer,
    },
)
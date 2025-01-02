from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from orders.serializers.create.create_order_serializer import CreateOrderSerializer
from orders.serializers.order_serializer import OrderSerializer
from orders.serializers.time_slot_serializer import CloseTimeSlotSerializer, TimeSlotSerializer
from orders.serializers.update_order_serializer import UpdateOrderSerializer

orders_schema = extend_schema_view(
    list=extend_schema(
        summary="List Orders",
        description="Retrieve a list of all orders.",
        responses={
            200: OrderSerializer(many=True)
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Order",
        description="Retrieve details of a specific order by ID.",
        responses={
            200: OrderSerializer,
        },
    ),
    create=extend_schema(
        summary="Create Order",
        description="Create a new order.",
        request=CreateOrderSerializer,
        responses={
            201: CreateOrderSerializer,
        },
    ),
    update=extend_schema(
        summary="Update Order",
        description="Update details of an existing order.",
        request=UpdateOrderSerializer,
        responses={
            200: UpdateOrderSerializer,
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Order",
        description="Partially update details of an existing order.",
        request=UpdateOrderSerializer,
        responses={
            200: UpdateOrderSerializer,
        },
    ),
    destroy=extend_schema(
        summary="Delete Order",
        description="Delete a Order.",
        responses={
            204: OpenApiResponse(description="Category deleted successfully."),
        },
    ),
)


#time slots schemas
close_time_slot_schema = extend_schema(
        summary="Close a time slot",
        description=(
            "This endpoint allows an admin to close a time slot for a provider. "
            "The slot will be marked as unavailable for booking."
        ),
        request=CloseTimeSlotSerializer,
        responses={
            200: OpenApiResponse(description="Slot closed successfully"),
            400: OpenApiResponse(description="Invalid data provided"),
        },
    )

closed_time_slots_list_schema = extend_schema(
        summary="Retrieve closed time slots",
        description=(
            "This endpoint retrieves all closed time slots for a specific provider on a specific date. "
            "The response contains all the slots that are unavailable for booking."
        ),
        responses={
            200: TimeSlotSerializer(many=True),
            400: OpenApiResponse(description="Missing or invalid parameters"),
        },
    )
from drf_spectacular.utils import extend_schema, extend_schema_view

from user.serializers.update_user_serializer import UpdateUserSerializer
from user.serializers.user_serializer import UserSerializer

user_schema = extend_schema_view(
    get=extend_schema(
        summary="Get User Details",
        description="Retrieves the details of the currently authenticated user.",
        responses={200: UserSerializer}
    ),
    post=extend_schema(
        summary="Update User Details",
        description="Updates the details of the currently authenticated user. Partial updates are supported.",
        request=UpdateUserSerializer,
        responses={
            200: {"type": "object", "properties": {"message": {"type": "string"}}},
        },
    ),
    delete=extend_schema(
        summary="Delete User Account",
        description="Deletes the currently authenticated user's account.",
        responses={
            204: {"type": "object", "properties": {"message": {"type": "string"}}},
        },
    ),
)
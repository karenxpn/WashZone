from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.decorators import validate_request
from user.serializers.update_user_serializer import UpdateUserSerializer
from user.serializers.user_serializer import UserSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
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

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @validate_request(UpdateUserSerializer)
    def post(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
        }, status=status.HTTP_200_OK)


    # DELETE: Delete the user
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({
            "message": "User deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

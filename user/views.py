from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from WashZone.presigned_url import generate_presigned_url
from authentication.decorators import validate_request
from user.schemas import user_schema, presigned_url_schema
from user.serializers.update_user_serializer import UpdateUserSerializer
from user.serializers.user_serializer import UserSerializer


@user_schema
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'presigned']

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



class PresignedURLView(APIView):
    permission_classes = [IsAuthenticated]

    @presigned_url_schema
    def post(self, request):
        file_name = request.data.get('file_name')
        file_type = request.data.get('file_type')

        return generate_presigned_url(file_name, file_type, 'users')

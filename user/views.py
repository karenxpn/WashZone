from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.decorators import validate_request
from user.schemas import user_schema
from user.serializers.update_user_serializer import UpdateUserSerializer
from user.serializers.user_serializer import UserSerializer
import boto3


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

    def post(self, request):
        file_name = request.data.get('file_name')
        file_type = request.data.get('file_type')

        if not file_name or not file_type:
            return Response({'message': 'Missing file_name or file_type'}, status=status.HTTP_400_BAD_REQUEST)

        s3 = boto3.client('s3')  # to be added the region name
        bucket_name = 'BucketName'  # to be added aws storage bucket name

        try:
            presigned_url = s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': f'users/{file_name}',
                    'ContentType': file_type
                },
                ExpiresIn=3600
            )

            return Response({'presigned_url': presigned_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

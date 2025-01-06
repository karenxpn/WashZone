import boto3
from rest_framework import status
from rest_framework.response import Response


def generate_presigned_url(file_name, file_type):
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
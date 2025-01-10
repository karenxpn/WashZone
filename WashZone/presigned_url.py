import uuid

import boto3
from rest_framework import status
from rest_framework.response import Response

from WashZone import settings


def generate_presigned_url(file_name, file_type, path):
    if not file_name or not file_type:
        return Response({'message': 'Missing file_name or file_type'}, status=status.HTTP_400_BAD_REQUEST)

    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_KEY,
                      region_name='us-east-2'
                      )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    try:
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': f'{path}/{uuid.uuid4()}_{file_name}',
                'ContentType': file_type
            },
            ExpiresIn=3600
        )

        return Response({'presigned_url': presigned_url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
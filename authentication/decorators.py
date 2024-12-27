from rest_framework.exceptions import APIException
from functools import wraps


def validate_request(serializer_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                request.validated_data = serializer.validated_data
                return func(self, request, *args, **kwargs)

            # Get first error message
            first_field = next(iter(serializer.errors))
            first_message = serializer.errors[first_field][0]
            raise APIException(detail={'message': f"{first_field}: {first_message}"})

        return wrapper

    return decorator
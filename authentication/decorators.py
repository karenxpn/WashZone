from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from functools import wraps

def validate_request(serializer_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                # Pass validated data to the view function
                request.validated_data = serializer.validated_data
                return func(self, request, *args, **kwargs)

            # Extract the first error message
            errors = serializer.errors
            first_error = next(iter(errors.values()))
            if isinstance(first_error, list):
                first_error = first_error[0]

            # Return formatted error response
            return Response({"message": str(first_error)}, status=status.HTTP_400_BAD_REQUEST)
        return wrapper
    return decorator


def validate_unexpected_fields(serializer_class):
    """
    A decorator to check for unexpected fields in the request data.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Check for unexpected fields
            expected_fields = set(serializer_class().fields.keys())
            unexpected_fields = [field for field in request.data if field not in expected_fields]

            if unexpected_fields:
                raise ValidationError(
                    {"message": f"Unexpected fields: {', '.join(unexpected_fields)}"}
                )

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

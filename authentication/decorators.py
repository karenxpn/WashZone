from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from functools import wraps


def validate_request(serializer_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data)

            # Check if serializer is valid
            if serializer.is_valid():
                # Pass validated data to the view function
                request.validated_data = serializer.validated_data
                return func(self, request, *args, **kwargs)

            # Collect and format error messages
            errors = serializer.errors
            formatted_errors = []

            for field, messages in errors.items():
                # Format the error message string
                for message in messages:
                    formatted_errors.append(f"{field}: {message.lower()}")

            # Return the formatted error response
            return Response({"message": " ".join(formatted_errors)}, status=status.HTTP_400_BAD_REQUEST)

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

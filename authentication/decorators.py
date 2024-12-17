from rest_framework.exceptions import ValidationError
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
                    formatted_errors.append(f"{field}: {message}")

            # raise the formatted error response
            raise ValidationError({"message": "\n".join(formatted_errors)})

        return wrapper

    return decorator
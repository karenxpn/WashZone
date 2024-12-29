from rest_framework.exceptions import ValidationError
from functools import wraps

def validate_request(serializer_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                request.validated_data = serializer.validated_data
                return func(self, request, *args, **kwargs)

            # Ensure serializer.errors exists and is a dictionary
            if not hasattr(serializer, "errors") or not isinstance(serializer.errors, dict):
                raise ValidationError({'message': 'Invalid error structure from serializer.'})

            # Get first error key
            first_field = next(iter(serializer.errors), None)
            if not first_field:
                raise ValidationError({'message': 'No error messages found in serializer.'})

            # Extract the error message dynamically
            first_message = serializer.errors[first_field]
            while isinstance(first_message, (list, dict)):
                if isinstance(first_message, list) and first_message:
                    first_message = first_message[0]
                elif isinstance(first_message, dict) and first_message:
                    first_message = next(iter(first_message.values()))
                else:
                    # Handle edge cases where the structure is empty
                    first_message = "An unknown error occurred."
                    break

            # Convert to string if not already
            if not isinstance(first_message, str):
                first_message = str(first_message)

            raise ValidationError({'message': f"{first_field}: {first_message}"})

        return wrapper

    return decorator

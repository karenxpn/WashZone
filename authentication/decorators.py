from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def validate_request_body(required_fields):
    """
    Decorator to validate the request body against required fields.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            data = request.data
            # Check for missing fields
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return Response(
                    {'error': f"Missing fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check for extra fields
            extra_fields = [field for field in data if field not in required_fields]
            if extra_fields:
                return Response(
                    {'error': f"Extra fields provided: {', '.join(extra_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Proceed to the actual function
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

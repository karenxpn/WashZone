from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    # Get the standard response from DRF
    response = exception_handler(exc, context)

    # Handle ValidationError exceptions
    if isinstance(exc, ValidationError) and response is not None:
        # Extract the first error message
        first_error = next(iter(response.data.values()))

        # Handle cases where the error is a list or a plain string
        if isinstance(first_error, list):
            first_error = first_error[0]

        response.data = {'message': str(first_error)}

    return response

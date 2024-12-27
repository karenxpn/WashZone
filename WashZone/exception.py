from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard response
    response = exception_handler(exc, context)

    if response is not None:
        # Extract the original data
        original_data = response.data

        # Replace all keys with 'message' while preserving their values
        response.data = {
            "message": list(original_data.values())[0]  # Take the first value as the message
        }

    return response

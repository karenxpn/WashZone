from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Keep message if it exists, otherwise format the error
        if isinstance(response.data, dict) and 'message' in response.data:
            response.data = {'message': response.data['message']}
        elif isinstance(response.data, dict) and 'detail' in response.data:
            response.data = {'message': response.data['detail']}

    return response
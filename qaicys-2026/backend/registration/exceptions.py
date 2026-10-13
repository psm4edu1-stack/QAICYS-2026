from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and not isinstance(response.data, dict):
        response.data = {"success": False, "errors": {"non_field_errors": response.data}}
    elif response is not None and "success" not in response.data:
        detail = response.data.pop("detail", None)
        response.data = {
            "success": False,
            "errors": {"non_field_errors": [str(detail)]} if detail else response.data,
        }
    return response

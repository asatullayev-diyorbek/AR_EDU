"""
Global DRF exception handler — wraps every error in the standard envelope.
"""
import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Call REST framework's default exception handler first to get the standard
    error response, then wrap it in our envelope.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # DRF handled it — rewrap
        error_detail = response.data
        if isinstance(error_detail, dict):
            message = _extract_message(error_detail)
        elif isinstance(error_detail, list):
            message = error_detail[0] if error_detail else "Validation error"
        else:
            message = str(error_detail)

        response.data = {
            "code": response.status_code,
            "message": str(message),
            "data": {},
        }
        logger.warning(
            "API error %s: %s — view: %s",
            response.status_code,
            message,
            context.get("view"),
        )
        return response

    # Unhandled exception — return 500
    logger.exception("Unhandled exception in %s", context.get("view"), exc_info=exc)
    return Response(
        {
            "code": 500,
            "message": "Internal server error. Please try again later.",
            "data": {},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _extract_message(detail: dict) -> str:
    """Flatten DRF validation error dicts into a human-readable string."""
    for key, value in detail.items():
        if isinstance(value, list) and value:
            return f"{key}: {value[0]}"
        if isinstance(value, str):
            return f"{key}: {value}"
        if isinstance(value, dict):
            return _extract_message(value)
    return "An error occurred"

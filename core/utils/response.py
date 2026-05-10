"""
Standardised API response helpers.

All API responses follow the shape:
    {
        "code":    <int>,
        "message": <str>,
        "data":    <any>
    }
"""
from rest_framework.response import Response


def success_response(data=None, message: str = "Success", code: int = 200) -> Response:
    """Return a DRF Response with the standard success envelope."""
    return Response(
        {
            "code": code,
            "message": message,
            "data": data if data is not None else {},
        },
        status=code,
    )


def error_response(message: str = "An error occurred", code: int = 400, data=None) -> Response:
    """Return a DRF Response with the standard error envelope."""
    payload = {
        "code": code,
        "message": message,
        "data": data if data is not None else {},
    }
    return Response(payload, status=code)


def paginated_response(paginator, serializer_class, queryset, request, message: str = "Success"):
    """
    Helper to combine DRF pagination with the standard envelope.

    Usage inside a ViewSet list() override:
        return paginated_response(self.pagination_class(), DeviceSerializer, qs, request)
    """
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serialized = serializer_class(page, many=True, context={"request": request})
        paginated = paginator.get_paginated_response(serialized.data)
        return Response(
            {
                "code": 200,
                "message": message,
                "data": paginated.data,
            },
            status=200,
        )

    serialized = serializer_class(queryset, many=True, context={"request": request})
    return success_response(data=serialized.data, message=message)

"""
Standardised API response helpers.
Every endpoint returns the same envelope shape so the Next.js frontend
can use a single Axios interceptor to handle success/error uniformly.

Shape:
  success: { "success": true,  "data": {...},   "message": "..." }
  error:   { "success": false, "errors": {...},  "message": "..." }
"""
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def success_response(data=None, message="", status_code=status.HTTP_200_OK):
    return Response(
        {"success": True, "message": message, "data": data},
        status=status_code,
    )


def error_response(message="An error occurred.", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response(
        {"success": False, "message": message, "errors": errors or {}},
        status=status_code,
    )


def created_response(data=None, message="Created successfully."):
    return success_response(data, message, status.HTTP_201_CREATED)


class EnvelopeMixin:
    """
    Mixin for DRF generic views that ensures list/retrieve responses
    are always wrapped in our standard success_response envelope.
    Add this as the FIRST base class on any generics.*View that doesn't
    already override list() or retrieve().
    """
    def retrieve(self, request, *args, **kwargs):
        return success_response(self.get_serializer(self.get_object()).data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler so all errors — including
    validation errors and 404s — return the same envelope shape.
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        original_data = response.data
        # DRF puts detail in either a string or a dict
        if isinstance(original_data, dict):
            message = original_data.pop("detail", "Validation error.")
            errors = original_data
        else:
            message = str(original_data)
            errors = {}

        response.data = {
            "success": False,
            "message": message,
            "errors": errors,
        }

    return response

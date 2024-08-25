from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def validate_query_params(query_name, valid_params):
    def decorator(func):
        @wraps(func)
        def wrapped(self, request, *args, **kwargs):
            query_params = request.query_params.get(query_name, None)

            if not query_params:
                return Response(
                    {
                        "message": f"No query parameters provided. Options are: {query_name}={valid_params}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if query_params not in valid_params:
                return Response(
                    {
                        "message": f"Invalid query parameter: {query_params}. Options are: {query_name}={valid_params}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return func(self, request, *args, **kwargs)

        return wrapped

    return decorator

"""
=====REST_FRAMEWORK Configurations=====
PERMISSIONS: DjangoModelPermissionsOrAnonReadOnly
AUTHENTICATION: BasicAuthentication, SessionAuthentication, JWTAuthentication
SCHEMA_CLASS: AutoSchema drf_spectacular
FILTER_BACKEND: DjangoFilterBackend
DEFAULT_PAGINATION_CLASS: PageNumber
"""

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "utils.extensions.custom_renderer.CustomJSONRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "utils.extensions.custom_pagination.CustomPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

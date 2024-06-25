# -------------------------------------
# DRF_SPECTACULAR CONFIGURATIONS
# -------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Potential Inc",
    "DESCRIPTION": "Potential Django Boilerplate API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SCHEMA_PATH_PREFIX": r"/api/",
    # "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.3",
    # OTHER SETTINGS
}

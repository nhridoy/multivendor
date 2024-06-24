import os
# -------------------------------------
# DJANGO: Configuration
# -------------------------------------
APP_CORS_HOSTS = os.getenv("CORS_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")
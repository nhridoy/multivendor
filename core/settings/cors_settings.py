import os
# -------------------------------------
# Cors: Configuration
# -------------------------------------
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_HOSTS").split(",")
CORS_ALLOW_CREDENTIALS = True

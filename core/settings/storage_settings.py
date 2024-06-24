from .base_settings import DEBUG, APP_MEDIA_ROOT, APP_STATIC_DIR, APP_STATIC_ROOT
import os


STATIC_URL = "static/"
STATIC_ROOT = APP_STATIC_ROOT
STATICFILES_DIRS = [APP_STATIC_DIR]

# DEFAULT_STORAGE = 'django.core.files.storage.FileSystemStorage'  # Default file storage

DEFAULT_FILE_STORAGE = (
    "storages.backends.s3.S3Storage"
    if not DEBUG
    else "django.core.files.storage.FileSystemStorage"
)

# STATICFILES_STORAGE = (
#     "storages.backends.s3.S3Storage"
#     if not DEBUG
#     else "django.contrib.staticfiles.storage.StaticFilesStorage"
# )
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")


STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
WHITENOISE_AUTOREFRESH = True

MEDIA_URL = "/media/"
MEDIA_ROOT = APP_MEDIA_ROOT
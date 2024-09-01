import os

USE_S3 = os.getenv("USE_S3") == "True"

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")  # AWS IAM user access key
    AWS_SECRET_ACCESS_KEY = os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    )  # AWS IAM user secret key
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")  # bucket name
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")  # region name
    AWS_S3_CUSTOM_DOMAIN = os.getenv(
        "CUSTOM_DOMAIN"
    )  # custom domain name from s3 or cloudfront
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }  # cache control settings
    AWS_QUERYSTRING_EXPIRE = int(
        os.getenv("AWS_QUERYSTRING_EXPIRE")
    )  # query string expire time
    AWS_LOCATION = f"{os.getenv('AWS_LOCATION')}"  # folder name in the bucket

    CLOUDFRONT_KEY_ID = os.getenv("CLOUDFRONT_KEY_ID")  # cloudfront key id
    AWS_CLOUDFRONT_KEY = os.getenv("AWS_CLOUDFRONT_KEY").replace(
        "\\n", "\n"
    )  # cloudfront private key

    # static files settings
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"  # static files url
    STATICFILES_STORAGE = "core.storages.s3.StaticFilesStorage"
    # public media settings
    DEFAULT_FILE_STORAGE = "core.storages.s3.PrivateMediaStorage"

else:
    STATIC_URL = "static/"
    STATIC_ROOT = "static/"

    MEDIA_ROOT = "media/"
    MEDIA_URL = "media/"

import os

# -------------------------------------
# REDIS: configurations
# -------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")


# -------------------------------------
# CHANNELS CONFIGURATION
# -------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}

# -------------------------------------
# CACHE CONFIGURATION
# -------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

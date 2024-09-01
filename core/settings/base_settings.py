import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_TEMPLATE_DIR = BASE_DIR.joinpath("templates")
APP_STATIC_DIR = BASE_DIR.joinpath("static")
APP_STATIC_ROOT = BASE_DIR.joinpath("staticfiles")
APP_MEDIA_ROOT = BASE_DIR.joinpath("media")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

PROJECT_NAME = os.getenv("PROJECT_NAME")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

FERNET_SECRET_KEY = os.getenv(
    "FERNET_SECRET_KEY", default="bhcTDnLm8eii39PHQ0g34uyDfxiSBIq__YQtPmufkFg="
)  # Encryption Secret Key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

# Application definition


INSTALLED_APPS = [
    "daphne",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Library packages
    "corsheaders",
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "drf_spectacular",
    "fcm_django",  # Firebase Cloud Messaging For push notifications
    "debug_toolbar",  # django debug toolbar
    "dj_rest_auth",
    "tinymce",
    "django_cleanup.apps.CleanupConfig",
    "storages",
    # created apps
    "authentications",
    "chat",
    "article",
    "forum",
    "support",
    "options",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentications.middleware.LanguageMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# AUTHENTICATION:  auth user model
AUTH_USER_MODEL = "authentications.User"

# WSGI_APPLICATION = "core.wsgi.application" # WSGI Application
ASGI_APPLICATION = "core.asgi.application"  # To run websockets use ASGI Application

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    # "authentications.auth_backend.EmailAuthenticationBackend",
    "social_core.backends.kakao.KakaoOAuth2",
    "social_core.backends.naver.NaverOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.github.GithubOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------
# DJANGO DEBUG TOOLBAR: Configurations
# -------------------------------------
INTERNAL_IPS = [
    "127.0.0.1",
]

USE_X_FORWARDED_HOST = os.getenv("USE_X_FORWARDED_HOST") == "True"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT") == "True"
if USE_X_FORWARDED_HOST and SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

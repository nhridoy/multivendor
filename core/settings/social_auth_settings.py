import os

GOOGLE_TOKEN_URL = os.getenv("GOOGLE_TOKEN_URL")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
GOOGLE_REDIRECT_URL = os.getenv("GOOGLE_REDIRECT_URL")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ["email", "profile"]

SOCIAL_AUTH_APPLE_ID_SERVICE = os.getenv("SOCIAL_AUTH_APPLE_ID_SERVICE")
SOCIAL_AUTH_APPLE_ID_CLIENT = os.getenv("SOCIAL_AUTH_APPLE_ID_CLIENT")
SOCIAL_AUTH_APPLE_ID_TEAM = os.getenv("SOCIAL_AUTH_APPLE_ID_TEAM")
SOCIAL_AUTH_APPLE_ID_SECRET = os.getenv("SOCIAL_AUTH_APPLE_ID_SECRET")
SOCIAL_AUTH_APPLE_ID_KEY = os.getenv("SOCIAL_AUTH_APPLE_ID_KEY")
SOCIAL_AUTH_APPLE_ID_SCOPE = ["email", "name"]
APPLE_TOKEN_URL = os.getenv("APPLE_TOKEN_URL")
APPLE_REDIRECT_URL = os.getenv("APPLE_REDIRECT_URL")

KAKAO_TOKEN_URL = os.getenv("KAKAO_TOKEN_URL")
SOCIAL_AUTH_KAKAO_KEY = os.getenv("SOCIAL_AUTH_KAKAO_KEY")
SOCIAL_AUTH_KAKAO_SECRET = os.getenv("SOCIAL_AUTH_KAKAO_SECRET")
SOCIAL_AUTH_KAKAO_SCOPE = ["account_email"]

NAVER_TOKEN_URL = os.getenv("NAVER_TOKEN_URL")
SOCIAL_AUTH_NAVER_KEY = os.getenv("SOCIAL_AUTH_NAVER_KEY")
SOCIAL_AUTH_NAVER_SECRET = os.getenv("SOCIAL_AUTH_NAVER_SECRET")

GITHUB_TOKEN_URL = os.getenv("GITHUB_TOKEN_URL")
SOCIAL_AUTH_GITHUB_KEY = os.getenv("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GITHUB_SCOPE = ["user:email"]


DEEPL_TRANSLATOR_API_KEY = os.getenv("DEEPL_TRANSLATOR_API_KEY")


SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

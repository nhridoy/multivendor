from .base_settings import env

# Authorize.net Payment Gateway
AUTHORIZE_NET_API_LOGIN_ID = env("AUTHORIZE_NET_API_LOGIN_ID", "")
AUTHORIZE_NET_TRANSACTION_KEY = env("AUTHORIZE_NET_TRANSACTION_KEY", "")
AUTHORIZE_NET_TRANSACTION_URL = env.url(
    "AUTHORIZE_NET_TRANSACTION_URL",
    default="https://apitest.authorize.net/xml/v1/request.api",
)

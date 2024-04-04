import pyotp
from django.conf import settings


class OTPVerification:
    secret_key: str

    def __init__(self, secret_key=settings.DEFAULT_OTP_SECRET, digit=4):
        self.totp = pyotp.TOTP(secret_key, interval=settings.OTP_TIME, digits=digit)

    def generate_otp(self):
        otp = self.totp.now()
        return otp

    def verify_otp(self, otp_code: str):
        return self.totp.verify(otp_code.strip())





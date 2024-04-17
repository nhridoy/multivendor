import pyotp
from django.conf import settings

from utils.modules import EmailSender


class OTPVerification:
    secret_key: str
    otp_code: str
    send_to: list[str]
    data = dict

    def __init__(self, secret_key=settings.DEFAULT_OTP_SECRET, digit=4):
        self.totp = pyotp.TOTP(secret_key, interval=settings.OTP_EXPIRY, digits=digit)

    def generate_otp(self):
        otp = self.totp.now()
        return otp

    def verify_otp(self, otp_code):
        return self.totp.verify(otp_code.strip())

    # def send_otp(self, send_to, name="User", company="Potential", procedure="Verification", valid_time="30 Min"):
    #     self.otp_code = self.generate_otp()
    #     email = EmailSender(subject="OTP Verification", send_to=send_to, context={"name": name, "company": company,
    #                                                                               "otp_code": self.otp_code,
    #                                                                               "procedure": procedure,
    #                                                                               "valid_time": valid_time},
    #                         template="email_templates/email_otp.html")
    #     self.data = {"otp_code": self.otp_code}
    #     return self.data

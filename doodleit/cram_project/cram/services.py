# create a otp here to use as extra security
import pyotp
import os
import time
from django.core.mail import send_mail

class OTP():

    def __init__(self):
        self.secret=pyotp.random_base32()
        self.totp=pyotp.TOTP(self.secret, interval=60)
    
    def generate(self):
        otp=self.totp.now()
        Emails.send_otp(otp)
        return otp
    
    def verifyToken(self, otp):
        is_valid=self.totp.verify(otp)
        return is_valid


class Emails():
    def send_otp(otp):
        send_mail(
            'user verification',
            f'here is your One-time password {otp}',
            'noreply@doodlr.com',
            ['example@example.com'],
            fail_silently=False
        )
        return send_mail
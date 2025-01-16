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
        return otp
    
    def verifyToken(self, otp):
        is_valid=self.totp.verify(otp)
        return is_valid


class Emails():
    def usernameChanged():
        email=send_mail(
            'change in account details',
            'youre username has been changed',
            'noreply@doodlr.com',
            'example@example.com'
        )
        return email
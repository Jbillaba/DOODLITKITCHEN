# create a otp here to use as extra security
import pyotp
import os
import time
from django.core.mail import send_mail

class OTP():

    def __init__(self):
        self.secret=pyotp.random_base32()
        self.totp=pyotp.TOTP(self.secret)
    
    def generate(self):
        otp=self.totp.now()
        return otp
    
    def verifyToken(self, otp):
        is_valid=self.totp.verify(otp)
        return is_valid

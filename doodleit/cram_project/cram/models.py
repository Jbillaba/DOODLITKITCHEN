from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timesince

class User(AbstractUser):
    username=models.CharField(max_length=20, unique=True)
    email=models.EmailField(max_length=40, unique=True)
    password=models.CharField(max_length=128)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Doodle(models.Model):
    image=models.FileField()
    created_on=models.DateTimeField(auto_now_add=True)
    doodlr=models.ForeignKey(User, on_delete=models.CASCADE, related_name='doodler')

    @property
    def timesince(self):
        return timesince.timesince(self.created_on)

    def __str__(self):
        return self.doodlr
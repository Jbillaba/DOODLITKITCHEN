from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timesince
defaultPicture='https://doodler-bucket.s3.us-east-2.amazonaws.com/default.jpg'

YEAH_CHOICES = {
    "HPY":"yeah!!",
    "NRM":"yeah",
    "SAD":"yeah..",
    "CFD":"yeah.?"
}

class User(AbstractUser):
    username=models.CharField(max_length=20, unique=True)
    profile_picture=models.FileField(default=defaultPicture)
    email=models.EmailField(max_length=40, unique=True)
    password=models.CharField(max_length=128)
    created_on=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Doodle(models.Model):
    title=models.CharField(max_length=40, default='')
    image=models.FileField()
    created_on=models.DateTimeField(auto_now_add=True)
    doodlr=models.ForeignKey(User, on_delete=models.CASCADE, related_name='doodler')

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Doodle, on_delete=models.CASCADE, related_name='originpost')
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentauthor')
    text=models.TextField(max_length=140)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Yeahs(models.Model):
    liker=models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
    post=models.ForeignKey(Doodle, on_delete=models.CASCADE, related_name='liked_post')
    type=models.CharField(max_length=6, choices=YEAH_CHOICES)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type


from django.db import models
import uuid
from django.db.models import UniqueConstraint, CheckConstraint
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

YEAH_CHOICES = {
    "HPY":"yeah!!",
    "NRM":"yeah",
    "SAD":"yeah..",
    "CFD":"yeah.?"
}

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_image=models.FileField(blank=True, null=True)
    username=models.CharField(max_length=20, unique=True)
    email=models.EmailField(max_length=40, unique=True)
    password=models.CharField(max_length=128)
    created_on=models.DateTimeField(auto_now_add=True)
    bio=models.CharField(max_length=60, default='', blank=True, null=True)
    pinned_doodle=models.ForeignKey('Doodle', on_delete=models.CASCADE, related_name='pinned_doodle', blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class UserOtp(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='opt_owner')
    otp=models.CharField(max_length=6, unique=True)
    is_valid=models.BooleanField(default=True)
    created_on=models.DateTimeField(auto_now_add=True)


class Doodle(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=40, default='')
    image=models.FileField()
    created_on=models.DateTimeField(auto_now_add=True)
    doodlr=models.ForeignKey(User, on_delete=models.CASCADE, related_name='doodler')
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post=models.ForeignKey(Doodle, on_delete=models.CASCADE, related_name='originpost')
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentauthor')
    text=models.TextField(max_length=140)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Yeahs(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    liker=models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
    post=models.ForeignKey(Doodle, on_delete=models.CASCADE, related_name='liked_post')
    type=models.CharField(max_length=6, choices=YEAH_CHOICES)
    created_on=models.DateTimeField(auto_now_add=True)
    
    class Meta: constraints=[
                UniqueConstraint(fields=['liker', 'post'], name='unique_yeah')
    ]

class UserFollows(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta: constraints=[
                UniqueConstraint(fields=['user_id', 'following_user_id'], name='unique_following'),
                CheckConstraint(check=~models.Q(user_id=models.F('following_user_id')), name='cannot_follow_self')
            ]
        
class savedDoodles(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_saved')
    doodle_id=models.ForeignKey(Doodle, on_delete=models.CASCADE, related_name='doodle_saved')

    class Meta: constraints=[
      UniqueConstraint(fields=['user_id', 'doodle_id'], name='unique_saves')
    ]
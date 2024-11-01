from .models import User, Doodle, Comment
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2=serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model=User
        fields=['username','email','password','password2']
    
    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError(
                {'password':"Password fields didn't match"}
            )

        return attrs
    
    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    account_created=serializers.SerializerMethodField("get_time_since_created")
    class Meta:
        model=User
        fields=['url','id', 'profile_picture' ,'username','email','account_created','password']
        extra_kwargs={
            'url': {'lookup_field': 'username'}
        }
    
    def get_time_since_created(self, object):
        return naturaltime(object.created_on)
    
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author=serializers.SerializerMethodField("get_author")
    post=serializers.SerializerMethodField("get_post_id")
    class Meta:
        model=Comment
        fields=['url', 'id', 'author','text', 'post','created_on']
    
    def get_author(self, object):
        return object.author.username
    
    def get_post_id(self, object):
        return object.post.id
    
    def create(self, validated_data):
        validated_data['author']=self.context['request'].user
        return super(CommentSerializer, self).create(validated_data)

class DoodleSerializer(serializers.HyperlinkedModelSerializer):
    content_type ='multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    doodlr=serializers.SerializerMethodField("get_doodler")
    created_on=serializers.SerializerMethodField("get_timesince")
    class Meta: 
        model=Doodle
        fields=['url','id','title','image','created_on','doodlr']

    def get_doodler(self, object):
        return object.doodlr.username
    
    def get_timesince(self, object):
        return naturaltime(object.created_on)
    
    def create(self, validated_data):
        validated_data['doodlr']=self.context['request'].user
        return super(DoodleSerializer, self).create(validated_data)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(
        
    )
    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')

        user=authenticate(
            request=self.context.get('request'),
            username=username, 
            password=password
        )

        if not user.password:
            msgPass=('incorrect password')
            raise serializers.ValidationError(msgPass, code='authentication')
        attrs['user']=user
        return attrs
        

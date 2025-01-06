from .models import User, Doodle, Comment, Yeahs, UserFollows
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth import authenticate
from django.db.models import Q, Count, Sum, Case, IntegerField, Sum, When

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
            password=validated_data['password'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    account_created=serializers.SerializerMethodField("get_time_since_created")
    num_of_doodles=serializers.SerializerMethodField("get_num_of_doodles")
    num_of_following=serializers.SerializerMethodField("get_num_of_following")
    num_of_followers=serializers.SerializerMethodField("get_num_of_followers")
    class Meta:
        model=User
        fields=['url','id','username','email','account_created', 'num_of_doodles', 'num_of_following', 'num_of_followers']

    def get_num_of_doodles(self, object):
        doodles=Doodle.objects.filter(doodlr=object.id).count()
        return doodles

    def get_time_since_created(self, object):
        return naturaltime(object.created_on)

    def get_num_of_following(self, object):
        following=UserFollows.objects.filter(user_id=object.id).count()
        return following

    def get_num_of_followers(self, object):
        follows=UserFollows.objects.filter(following_user_id=object.id).count()
        return follows

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author=serializers.SerializerMethodField("get_username")
    post_id=serializers.SerializerMethodField("get_post_id")
    created_on=serializers.SerializerMethodField("humanize_time")
    class Meta:
        model=Comment
        fields=['url', 'id', 'author','text', 'post', 'post_id', 'created_on']
    
    def get_username(self, object):
        return object.author.username
    
    def get_post_id(self, object):
        return object.post.id
    
    def humanize_time(self, object):
        return naturaltime(object.created_on)
    
    def create(self, validated_data):
        validated_data['author']=self.context['request'].user
        return super(CommentSerializer, self).create(validated_data)

class DoodleSerializer(serializers.HyperlinkedModelSerializer):
    content_type ='multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    doodlr=serializers.SerializerMethodField('get_doodlr_id')
    doodlr_username=serializers.SerializerMethodField("get_doodler")
    created_on=serializers.SerializerMethodField("get_timesince")
    number_of_comments=serializers.SerializerMethodField("get_number_of_comments")
    yeahs=serializers.SerializerMethodField("get_yeahs")
    class Meta: 
        model=Doodle
        fields=['url','id','title','image','created_on', 'doodlr' ,'doodlr_username','number_of_comments','yeahs']
    def get_doodlr_id(self, object):
        return object.doodlr.id

    def get_doodler(self, object):
        return object.doodlr.username
    
    def get_timesince(self, object):
        return naturaltime(object.created_on)
    
    def get_number_of_comments(self, object):
        comments=Comment.objects.filter(post=object.id).count()
        return comments
    
    def get_yeahs(self, object):
        yeahs=Yeahs.objects.filter(post_id=object.id).aggregate(
            hap=Count(
                'type', filter=Q(type='HPY')
            ),
            nrm=Count(
                'type', filter=Q(type='NRM')
            ),
            sad=Count(
                'type', filter=Q(type='SAD')
            ),
            cfd=Count(
                'type', filter=Q(type='CFD')
            ),
        )
        return yeahs

    def create(self, validated_data):
        validated_data['doodlr']=self.context['request'].user
        return super(DoodleSerializer, self).create(validated_data)

class YeahSerializer(serializers.HyperlinkedModelSerializer):
    created_on=serializers.SerializerMethodField('get_timesince')
    liker=serializers.SerializerMethodField("get_liker")
    class Meta:
        model=Yeahs
        fields=['url', 'id',  'liker', 'post', 'type', 'created_on']
    
    def get_timesince(self, object):
        return naturaltime(object.created_on)
    
    def get_liker(self, object):
        return object.liker.username

    def create(self, validated_data):
        validated_data['liker']=self.context['request'].user
        return super(YeahSerializer, self).create(validated_data)

class FollowsSerializer(serializers.HyperlinkedModelSerializer): 
    following_user=serializers.SerializerMethodField("get_following_username")
    following_id=serializers.SerializerMethodField("get_following_id")
    user_id=serializers.SerializerMethodField("get_id")
    username=serializers.SerializerMethodField("get_username")
    class Meta: 
        model=UserFollows
        fields=['url', 'id', 'user_id', 'username', 'following_user_id', 'following_user', 'following_id'] 

    def get_username(self, object):
        return object.user_id.username

    def get_following_username(self, object):
        return object.following_user_id.username

    def get_following_id(self, object):
        return object.following_user_id.id

    def get_id(self, object): 
        return object.user_id.id

    def create(self, validated_data):
        validated_data['user_id']=self.context['request'].user
        return super(FollowsSerializer, self).create(validated_data)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

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
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password=serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password']:
            raise serializers.ValidationError(
                {'passwords': 'passwords didnt match'}
            )
        return attrs
    
class DeleteAccountSerializer(serializers.Serializer):
    password=serializers.CharField(required=True)
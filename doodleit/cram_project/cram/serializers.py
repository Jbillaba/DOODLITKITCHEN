from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.humanize.templatetags.humanize import naturaltime

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2=serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model=User
        fields=['username',  'email', 'password', 'password2']
    
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
        fields=['url', 'id', 'username', 'email', 'account_created', 'password']
    
    def get_time_since_created(self, object):
        return naturaltime(object.created_on)
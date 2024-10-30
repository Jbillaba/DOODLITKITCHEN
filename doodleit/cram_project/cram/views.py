from rest_framework import viewsets, generics, filters
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User, Doodle, Comment
from .serializers import UserSerializer, RegisterSerializer, DoodleSerializer, LoginSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser

from knox.views import LoginView as KnoxLoginView

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=(AllowAny,)

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['username']
    search_fields=['username']
    lookup_field='username'

class DoodleViewSet(viewsets.ModelViewSet):
    queryset=Doodle.objects.all()
    serializer_class=DoodleSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    parser_classes=(MultiPartParser,)
    filter_backends=[filters.OrderingFilter]
    ordering_fields=['created_on']

class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['post__id']
    
class LoginView(KnoxLoginView):
    serializer_class=LoginSerializer
    permission_classes = (AllowAny,)
  
    def post(self, request, format=None):
        serializer=AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        login(request, user)
        response=super(LoginView, self).post(request, format=None)
    
        token=response.data['token']
        del response.data['token']
        
        response.set_cookie(
            'token',
            token,
            httponly=True,
            samesite=None
        )

        return response
from rest_framework import viewsets, generics, filters
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User, Doodle
from .serializers import UserSerializer, RegisterSerializer, DoodleSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
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
    ordering_fields=['username', 'name']
    search_fields=['username', 'name']

class DoodleViewSet(viewsets.ModelViewSet):
    queryset=Doodle.objects.all()
    serializer_class=DoodleSerializer
    permission_classes=(AllowAny,)
    filter_backends=[filters.OrderingFilter]
    ordering_fields=['created_on']
    
class LoginView(KnoxLoginView):
    serializer_class=LoginSerializer
    permission_classes = (AllowAny,)
  
    def post(self, request, format=None):
        serializer=AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
from rest_framework import viewsets, generics, filters
from .models import User, Doodle
from .serializers import UserSerializer, RegisterSerializer, DoodleSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=(AllowAny,)

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=(AllowAny,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['username', 'name']
    search_fields=['username', 'name']

class DoodleViewSet(viewsets.ModelViewSet):
    queryset=Doodle.objects.all()
    serializer_class=DoodleSerializer
    permission_classes=(AllowAny,)
    filter_backends=[filters.OrderingFilter]
    ordering_fields=['created_on']
    
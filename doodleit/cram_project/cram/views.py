from rest_framework import viewsets, generics, filters, views, status
from django.contrib.auth import login, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User, Doodle, Comment, Yeahs, UserFollows
from .serializers import UserSerializer, RegisterSerializer, DoodleSerializer, LoginSerializer, CommentSerializer, YeahSerializer, FollowsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from django.core.exceptions import ObjectDoesNotExist
import datetime

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

class CurrentUser(views.APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, format=None):
        user=User.objects.get(username=request.user)
        serializer_context={
            'request': request,
        }
        data=UserSerializer(user, context=serializer_context).data
        return Response(data)

class CurrentUserDoodles(views.APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, format=None):
        doodles=Doodle.objects.filter(doodlr=request.user)
        serializer_context={
            'request': request,
        }
        data=DoodleSerializer(doodles, context=serializer_context, many=True).data
        return Response(data)

class UserFollowsViewSet(viewsets.ModelViewSet):
    queryset=UserFollows.objects.all()
    serializer_class=FollowsSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['user_id']


class UserFollowingViewSet(UserFollowsViewSet):
    search_fields=['user_id__id']

class UserFollowersViewSet(UserFollowsViewSet):
    search_fields=['following_user_id__id']

class UserInFollowsView(views.APIView):
    permission_classes=(IsAuthenticated,) 
    def get(self, request, following_id):
        user=self.request.user
        target=self.kwargs['following_id']
        try:
            follow=UserFollows.objects.get(user_id=user, following_user_id_id=target)
            return Response("is following")
        except ObjectDoesNotExist:
            return Response("not following")
        

class DoodleViewSet(viewsets.ModelViewSet):
    queryset=Doodle.objects.all()
    serializer_class=DoodleSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    parser_classes=(MultiPartParser,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['doodlr__id']

class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['post__id']

class YeahViewSet(viewsets.ModelViewSet):
    queryset=Yeahs.objects.all()
    serializer_class=YeahSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
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
            expires=datetime.datetime.utcnow() + datetime.timedelta(days=6),
            httponly=True,
            samesite='None',
            secure=True,
        )
        return response

class LogoutView(views.APIView):
    def post(self, req, format=None):
        logout(req)
        response=Response({'details':'bye bye'})
        response.delete_cookie('token')
        return response

class isLoggedInView(views.APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, req, format=None):
        return Response("logged in")

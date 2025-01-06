from rest_framework import viewsets, generics, filters, views, status
from django.contrib.auth import login, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User, Doodle, Comment, Yeahs, UserFollows
from .serializers import UserSerializer, RegisterSerializer, DoodleSerializer, LoginSerializer, CommentSerializer, YeahSerializer, FollowsSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
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

    def partial_update(self, request, *args, **kwargs):
        user=self.get_object()
        if user != self.request.user:
            return Response("Not Allowed", status=status.HTTP_403_FORBIDDEN)
        serializer=UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("changes to profile made", status=status.HTTP_202_ACCEPTED)

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
            UserFollows.objects.get(user_id=user, following_user_id_id=target)
            return Response(True)
        except ObjectDoesNotExist:
            return Response(False)
       

class DoodleViewSet(viewsets.ModelViewSet):
    queryset=Doodle.objects.all()
    serializer_class=DoodleSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    parser_classes=(MultiPartParser,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['doodlr__id']

    def destroy(self, request, *args, **kwargs):
        doodle=self.get_object()
        if doodle.doodlr != self.request.user:
            return Response("not the owner"  ,status.HTTP_403_FORBIDDEN)
        doodle.delete()
        return Response("deleted", status=status.HTTP_202_ACCEPTED)
    
    def partial_update(self, request, *args, **kwargs):
        doodle=self.get_object()
        if doodle.doodlr != self.request.user:
            return Response("not the owner", status.HTTP_403_FORBIDDEN)
        serializer=DoodleSerializer(doodle, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("doodle edited", status=status.HTTP_202_ACCEPTED)
    
    def update(self, request, *args, **kwargs):
        doodle=self.get_object()
        if doodle.doodlr != self.request.user:
            return Response("not the owner", status=status.HTTP_403_FORBIDDEN)
        serializer=DoodleSerializer(doodle, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("updated", status=status.HTTP_202_ACCEPTED)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['post__id']

    def destroy(self, request, *args, **kwargs):
        comment=self.get_object()
        if comment.author != self.request.user:
            return Response("not the author", status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response("comment deleted", status=status.HTTP_202_ACCEPTED)
    
    def update(self, request, *args, **kwargs):
        comment=self.get_object()
        if comment.author != self.request.user:
            return Response("not the author", status=status.HTTP_403_FORBIDDEN)
        serializer=CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response("comment edited", status=status.HTTP_202_ACCEPTED)

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
            'uid',
            user.id,
            samesite='None',
            secure=True
        )
        response.set_cookie(
            'token',
            token,
            expires=datetime.datetime.now() + datetime.timedelta(days=6),
            httponly=True,
            samesite='None',
            secure=True,
        )
        return response

class LogoutView(views.APIView):
    def post(self, req, format=None):
        logout(req)
        response=Response({'details':'bye bye'})
        response.delete_cookie('uid')
        response.delete_cookie('token')
        return response

class isLoggedInView(views.APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, req, format=None):
        return Response("logged in")

class SearchView(views.APIView):
    permission_classes=(IsAuthenticatedOrReadOnly,)

    def get(self, request, query):
        search=self.kwargs['query']
        serializer_context={
            'request': request,
        }
        try: 
            doodles=Doodle.objects.filter(title__contains=search)
            doodleSerializer=DoodleSerializer(doodles, context=serializer_context, many=True).data

            users=User.objects.filter(username__contains=search)
            userSerializer=UserSerializer(users, context=serializer_context, many=True ).data
            
            result_list=chain(userSerializer, doodleSerializer)
            return Response(result_list)
        except ObjectDoesNotExist:
            return Response("search does not match anything")

class ChangePasswordView(views.APIView):
    serializer=ChangePasswordSerializer
    model=User
    permission_classes=(IsAuthenticated,)

    def get_object(self):
        return self.request.user
    
    def put(self, request):
        self.object=self.get_object()
        serializer=ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password=serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({'old_password': ['wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response={
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
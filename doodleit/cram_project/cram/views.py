from rest_framework import viewsets, generics, filters, views, status
from django.contrib.auth import login, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User, Doodle, Comment, Yeahs, UserFollows, UserOtp, savedDoodles, UUIDTaggedItem
from .serializers import UserSerializer, RegisterSerializer, DoodleSerializer, LoginSerializer, CommentSerializer, YeahSerializer, FollowsSerializer, ChangePasswordSerializer, DeleteAccountSerializer, OTPSerializer, UserOtpSerializer, SavedDoodlesSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
import datetime
from cram.services import OTP, Emails
from taggit.serializers import TaggitSerializer
Email=Emails()

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
    
    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user=self.get_object()
        token = request.COOKIES.get('ACP')
        
        if token != request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        if user != self.request.user:
            return Response("Not Allowed", status=status.HTTP_403_FORBIDDEN)
        serializer=UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("changes to profile made", status=status.HTTP_200_OK)

class CurrentUserDoodles(views.APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, format=None):
        serializer_context={
            'request': request,
            }
        try:
            pinned_doodle=Doodle.objects.filter(id=request.user.pinned_doodle.id)
            doodles=Doodle.objects.filter(doodlr=request.user).exclude(id=request.user.pinned_doodle.id)
            results=chain(pinned_doodle, doodles)
            data=DoodleSerializer(results, context=serializer_context, many=True).data
            return Response(data)
        except:
            doodles=Doodle.objects.filter(doodlr=request.user)
            data=DoodleSerializer(doodles, context=serializer_context, many=True).data
            return Response(data)


class UserFollowsViewSet(viewsets.ModelViewSet):
    queryset=UserFollows.objects.all()
    serializer_class=FollowsSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['user_id']

    def destroy(self, request, *args, **kwargs):
        follow=self.get_object()
        if follow.user_id != self.request.user:
            return Response("not allowed", status.HTTP_403_FORBIDDEN)
        follow.delete()
        return Response("unfollowed", status=status.HTTP_200_OK)
        
class UserFollowingViewSet(UserFollowsViewSet):
    search_fields=['user_id__id']

class UserFollowersViewSet(UserFollowsViewSet):
    search_fields=['following_user_id__id']

class UserInFollowsView(views.APIView):
    permission_classes=(IsAuthenticated,) 
    def get(self, request, query):
        user=self.request.user
        target=self.kwargs['query']
        try:
            follow=UserFollows.objects.get(user_id=user, following_user_id_id=target)
            serializer_context={
            'request': request,
            }
            serializer=FollowsSerializer(follow, context=serializer_context).data
            return Response(serializer, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)

class DoodleViewSet(viewsets.ModelViewSet):
    queryset=Doodle.objects.all()
    serializer_class=DoodleSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    parser_classes=(MultiPartParser,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['doodlr__id', 'tags__name']

    def destroy(self, request, *args, **kwargs):
        doodle=self.get_object()
        if doodle.doodlr != self.request.user:
            return Response("not the owner"  ,status.HTTP_403_FORBIDDEN)
        doodle.delete()
        return Response("deleted", status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        doodle=self.get_object()
        if doodle.doodlr != self.request.user:
            return Response("not the owner", status.HTTP_403_FORBIDDEN)
        serializer=DoodleSerializer(doodle, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("doodle edited", status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        doodle=self.get_object()
        if doodle.doodlr != self.request.user:
            return Response("not the owner", status=status.HTTP_403_FORBIDDEN)
        serializer=DoodleSerializer(doodle, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("updated", status=status.HTTP_200_OK)
    
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
        return Response("comment deleted", status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        comment=self.get_object()
        if comment.author != self.request.user:
            return Response("not the author", status=status.HTTP_403_FORBIDDEN)
        serializer=CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response("comment edited", status=status.HTTP_200_OK)

class YeahViewSet(viewsets.ModelViewSet):
    queryset=Yeahs.objects.all()
    serializer_class=YeahSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    filter_backends=[filters.OrderingFilter, filters.SearchFilter]
    ordering_fields=['created_on']
    search_fields=['post__id']

    def destroy(self, request, *args, **kwargs):
        yeah=self.get_object()
        if yeah.liker != self.request.user:
            return Response("not allowed", status=status.HTTP_403_FORBIDDEN)
        yeah.delete()
        return Response("unliked post", status=status.HTTP_200_OK)
    
class SavedDoodleViewSet(viewsets.ModelViewSet):
    queryset=savedDoodles.objects.all()
    serializer_class=SavedDoodlesSerializer
    permission_classes=(IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        saved_doodle=self.get_object()
        if saved_doodle.user_id != self.request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        saved_doodle.delete()
        return Response(status=status.HTTP_200_OK)

class CurrentUserSavedDoodles(views.APIView):
    permission_classes=(IsAuthenticated,)
    def get_user(self, request):
        return request.user

    def get(self, request):
        try:
            serializer_context={
            'request': request,
            }
            user=self.get_user(request)
            saved_doodles=savedDoodles.objects.filter(user_id=user)
            doodle_ids=saved_doodles.values_list('doodle_id', flat=True)
            list=Doodle.objects.filter(id__in=doodle_ids)
            serializer=DoodleSerializer(list, many=True, context=serializer_context).data
            return Response(serializer)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
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
            expires=datetime.datetime.now() + datetime.timedelta(days=6),
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
    def get(self, req, format=None):
        if 'token' and 'uid' not in req.COOKIES: 
            if 'uid' != req.user.id:
                return Response(False, status=status.HTTP_400_BAD_REQUEST)
            return Response(False, status=status.HTTP_401_UNAUTHORIZED)
        return Response(True, status=status.HTTP_200_OK)

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

            tags=Doodle.objects.filter(tags__name__contains=search)
            tagsSerializer=DoodleSerializer(tags, context=serializer_context, many=True).data

            users=User.objects.filter(username__contains=search)
            userSerializer=UserSerializer(users, context=serializer_context, many=True ).data
            
            result_list=chain(userSerializer, doodleSerializer, tagsSerializer)
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
        token = request.COOKIES.get('ACP')
        
        if token != request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

        if serializer.is_valid():
            old_password=serializer.data.get('old_password')
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

class DeleteAccountView(views.APIView):
    serializer=DeleteAccountSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

    def post(self, request):
        self.object=self.get_object()
        serializer=DeleteAccountSerializer(data=request.data)
        token = request.COOKIES.get('ACP')
        
        if token != request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
        if serializer.is_valid():
            password=serializer.data.get('password')
            if not self.object.check_password(password):
                return Response({'password': ['wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.delete()
            response={
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'account deleted succesfully',
                'data': []
            }
            response.delete_cookie('uid')
            response.delete_cookie('token')
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserOtpViewSet(viewsets.ModelViewSet):
    serializer_class=UserOtpSerializer
    queryset=UserOtp.objects.all()

class OtpGenerateView(views.APIView):
    permission_classes=(IsAuthenticated,)
    service=OTP()

    def post(self, request, format=None):
        otp=self.service.generate()
        try:
            UserOtp.objects.create(otp=otp, user=self.request.user)
            return Response("otp sent to email",status=status.HTTP_200_OK)
        except:
            return Response("something went wrong", status=status.HTTP_400_BAD_REQUEST)
    
class OtpAuthenticateView(views.APIView):
    permission_classes=(IsAuthenticated,)
    service=OTP()
    def patch(self, request, *args, **kwargs):
        serializer=OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp=serializer.data.get('otp')
        user_otp=UserOtp.objects.get(otp=otp)
        if user_otp.user != request.user or user_otp.is_valid != True:
            return Response("incorrect credentials", status=status.HTTP_400_BAD_REQUEST)
        try:
            self.service.verifyToken(otp)
            update_serializer=UserOtpSerializer(user_otp, data={"is_valid": False}, partial=True)
            update_serializer.is_valid(raise_exception=True)
            update_serializer.save()
            response = Response("correct credentials", status=status.HTTP_200_OK)
            response.set_cookie(
                'ACP',
                request.user.id,
                expires=datetime.datetime.now() + datetime.timedelta(minutes=15),
                samesite='None',
                secure=True
            )
            return response
        except:
            Response('incorrect credentials', status=status.HTTP_400_BAD_REQUEST)
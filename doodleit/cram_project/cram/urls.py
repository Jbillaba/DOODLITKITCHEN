from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from django.contrib import admin

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'doodles', views.DoodleViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'yeahs', views.YeahViewSet)
router.register(r'userFollows', views.UserFollowsViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')), 
    path('logged_in/', views.isLoggedInView.as_view(), name='check_auth-detail'),
    path('current_user/', views.CurrentUser.as_view(), name='current_user-detail'),
    path('current_doodles/', views.CurrentUserDoodles.as_view(), name='current_doodles-list'),
    path('user_following/', views.UserFollowingViewSet.as_view({'get':'list'}), name='user_following-list'),
    path('user_followers/', views.UserFollowersViewSet.as_view({'get':'list'}), name='user_followers-list'),
    path('user_in_following/', views.UserInFollowingViewSet.as_view({'get':'detail'}), name='user_in_following-detail'),
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', views.LogoutView.as_view(), name='knox_logout'),
]

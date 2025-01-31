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
router.register(r'userOtp', views.UserOtpViewSet)
router.register(r'savedDoodles', views.SavedDoodleViewSet)
router.register(r'tags', views.TagsViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('search/<str:query>/', views.SearchView.as_view(), name='search-list'),
    path('logged_in/', views.isLoggedInView.as_view(), name='check_auth-detail'),
    path('current_user/', views.CurrentUser.as_view(), name='current_user-detail'),
    path('current_doodles/', views.CurrentUserDoodles.as_view(), name='current_doodles-list'),
    path('user_following/', views.UserFollowingViewSet.as_view({'get':'list'}), name='user_following-list'),
    path('user_followers/', views.UserFollowersViewSet.as_view({'get':'list'}), name='user_followers-list'),
    path('is_following/<str:query>/', views.UserInFollowsView.as_view(), name='user_following-detail'),
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', views.LogoutView.as_view(), name='knox_logout'),
    path('token/', views.OtpGenerateView.as_view(), name='generate_token'),
    path('authenticate/', views.OtpAuthenticateView.as_view(), name='authenticate'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('delete_account/', views.DeleteAccountView.as_view(), name='delete_account'),
]
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from django.contrib import admin

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'doodles', views.DoodleViewSet)
router.register(r'comments', views.CommentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', views.LogoutView.as_view(), name='knox_logout'),
]

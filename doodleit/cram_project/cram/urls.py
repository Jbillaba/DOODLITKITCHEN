from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from django.contrib import admin
from .views import RegisterView
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'doodles', views.DoodleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/register/', RegisterView.as_view(), name='register_view')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
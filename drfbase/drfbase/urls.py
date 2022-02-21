"""drfbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from camsapp.views import CameraModelAPIView, CameraInfoModelAPIView
from django.conf import settings
from django.conf.urls.static import static
from srvapp.views import AIServerModelViewSet, CAMServerModelViewSet, ANServerModelViewSet

router = DefaultRouter()
router.register('cameras', CameraModelAPIView)
router.register('camerainfos', CameraInfoModelAPIView)
router.register('camservers', CAMServerModelViewSet)
router.register('aiservers', AIServerModelViewSet)
router.register('anservers', ANServerModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', include('camsapp.urls', namespace='camsapp')),
    path('srvapp/', include('srvapp.urls', namespace='srvapp')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

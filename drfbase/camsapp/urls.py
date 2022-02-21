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
from django.urls import path, include

from camsapp.views import IndexTemplateView, IndexDetailView, PictureUpdate, CameraModelDetailView

app_name = 'camsapp'
urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('cams/<int:pk>/', IndexDetailView.as_view(), name='camera'),
    path('camspic/<int:pk>/', PictureUpdate.as_view(), name='picture'),
    path('caminfo/<int:pk>/', CameraModelDetailView.as_view(), name='info'),
]

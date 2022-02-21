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
from srvapp.views import init_cam_server, action_cam_server, destroy_cam_server

app_name = 'srvapp'
urlpatterns = [
    path('cam/init/<int:pk>/', init_cam_server, name='caminit'),
    path('cam/action/<int:pk>/', action_cam_server, name='camaction'),
    path('cam/destroy/<int:pk>/', destroy_cam_server, name='camdestroy'),
]

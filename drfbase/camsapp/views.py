from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from camsapp.models import Camera
from camsapp.serializers import CameraModelSerializer


# Create your views here.
class CameraModelViewSet(ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraModelSerializer

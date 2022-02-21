from rest_framework.serializers import ModelSerializer
from camsapp.models import Camera, CameraInfo
from srvapp.models import CAMServer
from srvapp.serializers import AIServerForCameraModelSerializer, ANServerForCameraModelSerializer
from rest_framework import serializers


class CameraModelSerializer(ModelSerializer):
    aiserverinfo = AIServerForCameraModelSerializer(source='aiserver')
    anserverinfo = ANServerForCameraModelSerializer(source='anserver')

    class Meta:
        model = Camera
        exclude = ('users',)


class CameraInfoModelSerializer(ModelSerializer):
    class Meta:
        model = CameraInfo
        fields = '__all__'


class CameraInfoForAnModelSerializer(ModelSerializer):
    class Meta:
        model = CameraInfo
        exclude = ('camera', 'id',)

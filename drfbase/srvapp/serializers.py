from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from srvapp.models import AIServer, CAMServer, ANServer


class AIServerModelSerializer(ModelSerializer):
    class Meta:
        model = AIServer
        fields = '__all__'


class ANServerModelSerializer(ModelSerializer):
    class Meta:
        model = ANServer
        fields = '__all__'


class CAMServerModelSerializer(ModelSerializer):
    class Meta:
        model = CAMServer
        fields = '__all__'


class AIServerForCameraModelSerializer(ModelSerializer):
    class Meta:
        model = AIServer
        exclude = ('id',)


class ANServerForCameraModelSerializer(ModelSerializer):
    class Meta:
        model = ANServer
        exclude = ('id',)

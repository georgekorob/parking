from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from srvapp.models import AIServer


class AIServerModelSerializer(ModelSerializer):
    class Meta:
        model = AIServer
        fields = '__all__'


class AIServerForCameraModelSerializer(ModelSerializer):
    class Meta:
        model = AIServer
        exclude = ('id',)

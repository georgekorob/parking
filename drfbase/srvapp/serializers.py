from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from srvapp.models import AIServer


class AIServerModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AIServer
        fields = '__all__'

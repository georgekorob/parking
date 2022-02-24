from rest_framework.serializers import ModelSerializer
from fisheyeapp.models import CameraFish


class CameraFishModelSerializer(ModelSerializer):
    class Meta:
        model = CameraFish
        fields = '__all__'

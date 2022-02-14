from rest_framework.serializers import ModelSerializer
from camsapp.models import Camera


class CameraModelSerializer(ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

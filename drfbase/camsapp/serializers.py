from rest_framework.serializers import ModelSerializer
from camsapp.models import Camera


class CameraModelSerializer(ModelSerializer):
    class Meta:
        model = Camera
        fields = ('id',
                  'cam_server_id',
                  'ip_addr',
                  'port',
                  'slug_after',
                  'username',
                  'password',
                  'picture')

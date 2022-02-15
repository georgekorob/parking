from rest_framework.serializers import HyperlinkedModelSerializer
from camsapp.models import Camera
from srvapp.serializers import AIServerModelSerializer


class CameraModelSerializer(HyperlinkedModelSerializer):
    url_ai = AIServerModelSerializer(source="ai_server")

    class Meta:
        model = Camera
        exclude = ('users',)
        # fields = ('id',
        #           'cam_server',
        #           'ai_server',
        #           'url',
        #           'picture')

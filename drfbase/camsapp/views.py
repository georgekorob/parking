from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from camsapp.models import Camera, CameraInfo
from camsapp.serializers import CameraModelSerializer, CameraInfoModelSerializer, CameraInfoForAnModelSerializer
from srvapp.views import action_cam_server


# Create your views here.
class CameraModelAPIView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraModelSerializer
    filterset_fields = ['camserver']

    def partial_update(self, request, *args, **kwargs):
        # TODO:
        # 1. Если в запросе есть точки парковочных мест, то удалить текущие и создать новые
        # 2. Подать запрос action_cam_server(request, pk)
        return super().partial_update(request, *args, **kwargs)


class IndexTemplateView(TemplateView):
    template_name = 'camsapp/index.html'


class IndexDetailView(DetailView):
    template_name = 'camsapp/camera.html'
    model = Camera


class PictureUpdate(DetailView):
    model = Camera
    fields = []

    def render_to_response(self, context, **response_kwargs):
        result = render_to_string('camsapp/image.html', context)
        return JsonResponse({'result': result})


class CameraInfoModelAPIView(ModelViewSet):
    queryset = CameraInfo.objects.all()
    serializer_class = CameraInfoModelSerializer


class CameraModelDetailView(DetailView):
    model = Camera

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        camerainfo = CameraInfoForAnModelSerializer(self.object.info.get()).data
        return JsonResponse(camerainfo)

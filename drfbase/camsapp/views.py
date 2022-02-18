from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from camsapp.models import Camera
from camsapp.serializers import CameraModelSerializer


# Create your views here.
class CameraModelAPIView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraModelSerializer
    filterset_fields = ['camserver']

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


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

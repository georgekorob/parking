from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView, UpdateView
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from fisheyeapp.models import CameraFish
from fisheyeapp.serializers import CameraFishModelSerializer


# Create your views here.
class FishModelViewSet(ModelViewSet):
    queryset = CameraFish.objects.all()
    serializer_class = CameraFishModelSerializer


class FishDetailView(DetailView):
    template_name = 'fisheyeapp/camfish.html'
    model = CameraFish


def update_tables_fish(request, pk):
    camerafish = get_object_or_404(CameraFish, pk=pk)
    camera = camerafish.camera
    context = {}
    result = render_to_string('fisheyeapp/image.html', context)
    return JsonResponse({'result': result})

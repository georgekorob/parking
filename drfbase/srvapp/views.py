import requests, socket
from django.core.exceptions import BadRequest
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from camsapp.models import Camera
from camsapp.serializers import CameraModelSerializer
from camsapp.views import CameraModelAPIView
from srvapp.models import AIServer, CAMServer
from srvapp.serializers import AIServerModelSerializer, CAMServerModelSerializer, AIServerForCameraModelSerializer, \
    ANServerForCameraModelSerializer


# Create your views here.
class AIServerModelViewSet(ModelViewSet):
    queryset = AIServer.objects.all()
    serializer_class = AIServerModelSerializer


def post_request_to_cam(request, ip, port, command, data=None):
    try:
        data_json = JSONRenderer().render(data)
        response = requests.post(f'http://{ip}:{port}/{command}/', data=data_json)
        if response.status_code != 200:
            raise BadRequest(response.status_code)
    except Exception as e:
        print(e)
    finally:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def init_cam_server(request, pk):
    cam_server = get_object_or_404(CAMServer, pk=pk)
    cameras = cam_server.camera_set.all()
    data_cams = []
    for camera in cameras:
        data = CameraModelSerializer(camera).data
        data['aiserverinfo'] = AIServerForCameraModelSerializer(data['aiserverinfo']).data
        data['anserverinfo'] = ANServerForCameraModelSerializer(data['anserverinfo']).data
        data_cams.append(data)
    return post_request_to_cam(request, cam_server.ip, cam_server.port, 'init', data_cams)


def action_cam_server(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    cam_server = camera.camserver
    return post_request_to_cam(request, cam_server.ip, cam_server.port, 'action', [camera.id])


def destroy_cam_server(request, pk):
    cam_server = get_object_or_404(CAMServer, pk=pk)
    return post_request_to_cam(request, cam_server.ip, cam_server.port, 'destroy')

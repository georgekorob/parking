from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from srvapp.models import AIServer
from srvapp.serializers import AIServerModelSerializer


# Create your views here.
class AIServerModelViewSet(ModelViewSet):
    queryset = AIServer.objects.all()
    serializer_class = AIServerModelSerializer

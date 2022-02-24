from django.db import models
from camsapp.models import Camera


# Create your models here.
class CameraFish(models.Model):
    camera = models.OneToOneField(Camera, related_name='fish', on_delete=models.CASCADE)
    fisheye = models.TextField(default='')

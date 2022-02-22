from django.db import models
from authapp.models import User
from srvapp.models import CAMServer, AIServer, ANServer


# Create your models here.
class Camera(models.Model):
    camserver = models.ForeignKey(CAMServer, on_delete=models.CASCADE)
    aiserver = models.ForeignKey(AIServer, on_delete=models.CASCADE)
    anserver = models.ForeignKey(ANServer, on_delete=models.CASCADE)
    baseserverlink = models.URLField(blank=True)
    camlink = models.URLField(blank=True)
    picture = models.ImageField(upload_to='camerashots')
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.id:05d} camera'

    class Meta:
        verbose_name = 'камера'
        verbose_name_plural = 'камеры'


class CameraInfo(models.Model):
    camera = models.OneToOneField(Camera, related_name='info', on_delete=models.CASCADE)
    camerainfo = models.TextField(default='')


class CarPoint(models.Model):
    camera = models.ForeignKey(Camera, related_name='points', on_delete=models.CASCADE)
    xmap = models.IntegerField(default=0)
    ymap = models.IntegerField(default=0)
    xframe = models.IntegerField(default=0)
    yframe = models.IntegerField(default=0)
    is_busy = models.BooleanField(default=True)

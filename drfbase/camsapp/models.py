from django.db import models
from authapp.models import User
from srvapp.models import CAMServer, AIServer


# Create your models here.
class Camera(models.Model):
    camserver = models.ForeignKey(CAMServer, on_delete=models.CASCADE)
    aiserver = models.ForeignKey(AIServer, on_delete=models.CASCADE)
    camlink = models.URLField(blank=True)
    picture = models.ImageField(upload_to='camerashots')
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.id:05d} camera'

    class Meta:
        verbose_name = 'камера'
        verbose_name_plural = 'камеры'

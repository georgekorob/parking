from django.db import models
from authapp.models import User
from srvapp.models import CAMServer, AIServer


# Create your models here.
class Camera(models.Model):
    cam_server = models.ForeignKey(CAMServer, on_delete=models.CASCADE)
    ai_server = models.ForeignKey(AIServer, on_delete=models.CASCADE)
    # ip_addr = models.GenericIPAddressField()
    # port = models.PositiveIntegerField(default=554)
    # slug_after = models.CharField(default='av0_1', max_length=128)
    # username = models.CharField(max_length=64)
    # password = models.CharField(max_length=64)
    url = models.URLField(blank=True)
    users = models.ManyToManyField(User)
    picture = models.ImageField(upload_to='camerashots')

    def __str__(self):
        return f'{self.id:05d} camera'

    class Meta:
        verbose_name = 'камера'
        verbose_name_plural = 'камеры'

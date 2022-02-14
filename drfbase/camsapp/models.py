from django.db import models
from authapp.models import User


# Create your models here.
class Camera(models.Model):
    cam_server_id = models.IntegerField(default=1)
    ip_addr = models.GenericIPAddressField()
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.id:02d}. Camera {self.ip_addr}'

    class Meta:
        verbose_name = 'камера'
        verbose_name_plural = 'камеры'

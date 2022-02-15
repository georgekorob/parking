from django.db import models


# Create your models here.
class CAMServer(models.Model):
    name = models.CharField(max_length=32)


class AIServer(models.Model):
    name = models.CharField(max_length=32)
    ip_address = models.CharField(max_length=16)
    port = models.PositiveIntegerField(default=8001)

    def __str__(self):
        return f'http://{self.ip_address}:{self.port}/'

    class Meta:
        verbose_name = 'ai сервер'
        verbose_name_plural = 'ai сервера'


class ANServer(models.Model):
    name = models.CharField(max_length=32)

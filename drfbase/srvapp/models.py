from django.db import models


class ParkingServerMixin(models.Model):
    servername = models.CharField(max_length=32)
    ip = models.CharField(max_length=16)
    port = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True


# Create your models here.
class CAMServer(ParkingServerMixin):
    class Meta:
        verbose_name = 'cam сервер'
        verbose_name_plural = 'cam сервера'


class AIServer(ParkingServerMixin):
    def __str__(self):
        return f'http://{self.ip}:{self.port}/'

    class Meta:
        verbose_name = 'ai сервер'
        verbose_name_plural = 'ai сервера'


class ANServer(ParkingServerMixin):
    class Meta:
        verbose_name = 'an сервер'
        verbose_name_plural = 'an сервера'

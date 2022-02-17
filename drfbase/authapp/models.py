from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


# Create your models here.
class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    email = models.EmailField(unique=True)
    gender = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=2)
    birth = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

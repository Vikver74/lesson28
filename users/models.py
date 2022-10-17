from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=60, verbose_name='Наименование')
    lat = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='Широта', null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='Долгота', null=True)

    def __str__(self):
        return [self.name, self.lat, self.lng]

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'


class User(AbstractUser):
    ROLE = [
        ('member', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    ]
    role = models.CharField(max_length=10, default='member', choices=ROLE)
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ManyToManyField(Location, related_name='users')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


def validate_age(birth_date:date):
    now_date: date = date.today()
    age: int = now_date.year - birth_date.year
    if birth_date.month > now_date.month:
        age -= 1
    elif birth_date.month == now_date.month and birth_date.day > now_date.day:
        age -= 1

    if age < 9:
        raise ValidationError('Age less than 9 year')


def validate_email_(mail):
    if mail.endswith('rambler.ru'):
        raise ValidationError('Domain rambler.ru prohibited')
    return mail


class Location(models.Model):
    name = models.CharField(max_length=60, verbose_name='Наименование')
    lat = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='Широта', null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='Долгота', null=True)

    def __str__(self):
        return self.name

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
    birth_date = models.DateField(validators=[validate_age])
    email = models.EmailField(max_length=60, validators=[validate_email_], unique=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

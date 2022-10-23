import django.core.validators as validator
from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


def validate_positive_number(value):
    if value < 0:
        raise ValidationError("Value cannot be less than zero")
    return value


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=10, validators=[validator.MinLengthValidator(5)], unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=50, validators=[validator.MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    price = models.IntegerField(validators=[validate_positive_number])
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='ads')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class SelectionAd(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selections')
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.name

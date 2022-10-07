from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    price = models.IntegerField()
    description = models.TextField(null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='ads')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'





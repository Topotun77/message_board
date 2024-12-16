from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    """
    Выбор директории загрузки в зависимости от id пользователя
    """
    try:
        file = f'images/user_{instance.author.id}/{filename}'
    except:
        file = f'images/user_{instance.user.id}/{filename}'
    return file


class Advertisement(models.Model):
    """
    Модель таблица Объявления
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Image(models.Model):
    """
    Модель таблицы изображений
    """
    advertisement = models.ForeignKey(Advertisement, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Файл', blank=True, null=True)

    def __str__(self):
        return self.image.name


class Comment(models.Model):
    """
    Модель таблицы комментариев к объявлениям
    """
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'


class Preferences(models.Model):
    """
    Модель таблицы пользовательских настроек
    """
    themes = (
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
    )

    preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    theme = models.CharField(max_length=255, choices=themes)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='Одна запись на пользователя')
        ]

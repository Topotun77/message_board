from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    """
    Модель таблица Объявления
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель таблицы комментариев к объявлениям
    """
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
            models.UniqueConstraint(fields=['user'], name='One Entry Per User')
        ]

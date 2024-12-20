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
    """  Модель таблица Объявления  """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Image(models.Model):
    """  Модель таблицы изображений  """
    advertisement = models.ForeignKey(Advertisement, related_name='images', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return f'Картинка к объявлению {self.advertisement}. Файл {self.image.name}.'

    class Meta:
        verbose_name = 'Изображения'
        verbose_name_plural = 'Изображения'


class Comment(models.Model):
    """  Модель таблицы комментариев к объявлениям  """
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} на объявление "{self.advertisement}"'


class Like(models.Model):
    """  Модель лайков/дизлайков пользователей  """
    like_types = (
        (0, 'DisLike'),
        (1, 'Like'),
    )

    advertisement = models.ForeignKey(Advertisement, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_type = models.IntegerField(choices=like_types, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лайки-дизлайки'
        verbose_name_plural = 'Лайки-дизлайки'

    def __str__(self):
        return f'Объявление "{self.advertisement}", {self.get_like_type_display()} от {self.user}'


class UserStat(models.Model):
    """  Модель статистики по пользователям  """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    advertisement_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

    def __str__(self):
        return (f'Пользователь {self.user}: '
                f'сообщений {self.advertisement_count}, '
                f'лайков {self.like_count}, '
                f'дизлайков {self.dislike_count}')


class Preferences(models.Model):
    """  Модель таблицы пользовательских настроек  """
    themes = (
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
    )

    preference_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)

    theme = models.CharField(max_length=255, choices=themes)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='Одна запись на пользователя')
        ]

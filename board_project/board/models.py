from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'


# class ThemeConfiguration(models.Model):
#     THEME = [
#         (True, _('dark')),
#         (False, _('light')),
#     ]
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     theme = models.BooleanField(_('theme'),
#        default=True)
#
#     class Meta:
#        constraints = [
#            models.UniqueConstraint(fields=['user'], name='One Entry Per User')
#        ]
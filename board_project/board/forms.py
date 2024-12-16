from django import forms
from django.utils.safestring import mark_safe

from .models import Advertisement, Image, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertisementForm(forms.ModelForm):
    """
    Форма для объявлений
    """
    title = forms.CharField(label='Заголовок объявления:', max_length=200)
    content = forms.CharField(label='Текст объявления:', widget=forms.Textarea, empty_value='')
    # images = forms.FileField(label='Изображения:',
    #                          widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #                          help_text='Загрузите картинки при необходимости.',
    #                          required=False)
    image = forms.ImageField(label='Изображение:', help_text='Загрузите картинку при необходимости.', required=False)

    class Meta:
        model = Advertisement
        readonly_fields = ['preview']
        fields = ['title', 'content', 'image']

        def preview(self, obj):
            return mark_safe(f"<img src='{obj.image.url}' height='300'>")

class CommentForm(forms.ModelForm):
    """
    Форма для комментариев
    """
    content = forms.CharField(label='Текст комментария:', widget=forms.Textarea, empty_value='')

    class Meta:
        model = Comment
        fields = ['content']


class ImageForm(forms.ModelForm):
    """
    Форма для загрузки картинок
    """
    image_path = forms.ImageField(label='Изображение:', help_text='Загрузите картинку при необходимости.',
                                  required=False)

    class Meta:
        model = Image
        fields = ['image_path']


class SignUpForm(UserCreationForm):
    """
    Форма для регистрации пользователей
    """
    username = forms.CharField(label='Ник пользователя:')
    first_name = forms.CharField(label='Имя пользователя (не обязательно):', required=False)
    password1 = forms.CharField(label='Введите пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2',)

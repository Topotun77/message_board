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
    image = forms.ImageField(label='Изображение:', help_text='Загрузите картинку при необходимости.', required=False)

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image']


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
    image = forms.ImageField(label='Изображение:')

    class Meta:
        model = Image
        fields = ['image']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ImageForm2(forms.ModelForm):
    """
    Форма для загрузки картинок 2
    """
    photo = MultipleFileField(label='Выберите файлы:', required=False)

    class Meta:
        model = Image
        fields = ['photo', ]


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

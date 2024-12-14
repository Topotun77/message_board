from django import forms
from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertisementForm(forms.ModelForm):
    """
    Форма для объявлений
    """
    title = forms.CharField(label='Заголовок объявления:', max_length=200)
    content = forms.CharField(label='Текст объявления:', widget=forms.Textarea, empty_value='')
    image = forms.ImageField(label='Изображение:', help_text='Загрузите картинку при необходимости.')

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'image']

class SignUpForm(UserCreationForm):
    """
    Форма для регистрации пользователей
    """
    username = forms.CharField(label='Имя пользователя:')
    password1 = forms.CharField(label='Введите пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

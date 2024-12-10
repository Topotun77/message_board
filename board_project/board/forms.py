from django import forms
from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertisementForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок объявления:', max_length=200)
    content = forms.CharField(label='Текст объявления:', widget=forms.Textarea)

    class Meta:
        model = Advertisement
        fields = ['title', 'content']


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя:')
    password1 = forms.CharField(label='Введите пароль:')
    password2 = forms.CharField(label='Повторите пароль:')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

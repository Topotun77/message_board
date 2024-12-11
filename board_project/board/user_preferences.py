from django.http import HttpRequest
from .models import Preferences


def pref(request: HttpRequest):
    """
    Считывает пользовательские предпочтения, в случае, если было нажатие на элемент
    переключения темы (темной/светлой), меняет тему на противоположную
    :param request: HttpRequest - запрос пользователя
    :return: Пользовательские предпочтения
    """
    if request.user.is_authenticated:
        _preferences = Preferences.objects.filter(user=request.user).last()
        if request.GET.get('day') == 'theme':
            if _preferences.theme is None:
                Preferences.objects.create(user=request.user, theme='dark')
            elif _preferences.theme == 'light':
                Preferences.objects.update(user=request.user, theme='dark')
            else:
                Preferences.objects.update(user=request.user, theme='light')
            _preferences = Preferences.objects.filter(user=request.user).last()
    else:
        _preferences = None
    return {
        'user_pref': _preferences,
    }

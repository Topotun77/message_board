import asyncio
import logging
import os
from django.http import HttpRequest

from .models import Like, Advertisement
from .kandinsky import gen


def decor_log(func):
    """
    Декоратор для ведения логирования
    :return: полученную обернутую функцию
    """
    def log_writer(*args, **kwargs):
        rez = func(*args, **kwargs)
        str_ = f'{func.__name__}: {rez}'
        logging.info(str_)
        return rez

    return log_writer


def like_read(request: HttpRequest, pk: int) -> dict:
    """
    Узнать количество лайков и дизлайков на выбранном сообщении
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: Словарь с количеством лайков и дизлайков
    """
    context = {}
    if request.user.is_authenticated:
        count_like = len(Like.objects.filter(advertisement=pk, user=request.user.id, like_type=1))
        if count_like:
            context['like'] = count_like
        count_like = len(Like.objects.filter(advertisement=pk, user=request.user.id, like_type=0))
        if count_like:
            context['dislike'] = count_like
    return context


def like_set(request: HttpRequest, pk: int, tp: int):
    """
    Поставить или убрать лайк/дизлайк
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :param tp: Тип лайка (1 - лайк, 0 - дизлайк)
    """
    if request.user.is_authenticated:
        advertisement = Advertisement.objects.get(pk=pk)
        like = Like.objects.filter(advertisement=pk, user=request.user.id, like_type=1).first()
        dislike = Like.objects.filter(advertisement=pk, user=request.user.id, like_type=0).first()
        if tp == 1:
            if like:
                like.delete()
                advertisement.like_count = int(advertisement.like_count) - 1
            else:
                Like.objects.create(advertisement=advertisement, user=request.user, like_type=1)
                advertisement.like_count = int(advertisement.like_count) + 1
                if dislike:
                    dislike.delete()
                    advertisement.dislike_count = int(advertisement.dislike_count) - 1
            advertisement.save()
        if tp == 0:
            if dislike:
                dislike.delete()
                advertisement.dislike_count = int(advertisement.dislike_count) - 1
            else:
                Like.objects.create(advertisement=advertisement, user=request.user, like_type=0)
                advertisement.dislike_count = int(advertisement.dislike_count) + 1
                if like:
                    like.delete()
                    advertisement.like_count = int(advertisement.like_count) - 1
            advertisement.save()
    return


def kandinsky_query(text: str = 'пустота', dir_='./', file_='image.jpg') -> str:
    """
    Отправка и обработка запроса на генерацию картинки Kandinsky 3.0
    :param text: текст запроса
    :param dir_: Директория вывода.
    :param file_: Файл вывода.
    :return: картеж, содержащий имя сформированного файла и текст самого запроса
    для логирования
    """

    try:
        os.mkdir(dir_)
    except FileExistsError:
        print('exist')
        # file_name = await kandinsky.gen(text.replace("\n", " "), dir_)  #TODO асинхронность
    try:
        file_name = asyncio.run(gen(text.replace("\n", " "), dirr=dir_, file_name=file_))

    except Exception as err:
        file_name_cut = f'Error: {err.args}'
    return

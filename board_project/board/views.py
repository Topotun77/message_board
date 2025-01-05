import logging
import os
import shutil
import time
from datetime import datetime
# from multiprocessing import Process
from threading import Thread

from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from .models import Advertisement, Image, Comment, Like, UserStat, Preferences
from .forms import AdvertisementForm, CommentForm, ImageForm, PreferencesForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from .utilite import like_read, like_set, kandinsky_query, read_pade_count


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление - Выход из системы (logout)
    :param request: HttpRequest - запрос пользователя
    :return: HttpResponseRedirect - перенаправление на домашнюю страницу
    """
    logout(request)
    return redirect('login')


def signup(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление - Регистрация пользователя
    :param request: HttpRequest - запрос пользователя
    :return: После регистрации перенаправление на страницу с объявлениями
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            logging.info(f'Создан пользователь: {user}')
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление - Регистрация пользователя.
    :param request: HttpRequest - запрос пользователя.
    :return: После регистрации перенаправление на страницу с объявлениями.
    """
    return render(request, 'home.html')


def user_stat_list(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление - Просмотр статистики по пользователям.
    :param request: HttpRequest - запрос пользователя.
    :return: Остаемся на странице.
    """
    user_stat = UserStat.objects.all()
    return render(request, 'board/user_statistic_list.html', {'user_stat': user_stat})


def user_settings(request: HttpRequest) -> HttpResponseRedirect:
    """
    Изменить пользовательские настройки.
    :param request: HttpRequest - запрос пользователя.
    :return: Остаемся на странице.
    """
    user_stat = UserStat.objects.all()
    try:
        pref = Preferences.objects.get(user=request.user)
    except BaseException as er:
        logging.error(f'user_settings: {er}')
        Preferences.objects.create(user=request.user)
        pref = Preferences.objects.get(user=request.user)
    if request.method == "POST":
        form = PreferencesForm(request.POST, request.FILES, instance=pref)
        if form.is_valid():
            user_sett = form.save(commit=False)
            user_sett.user = request.user
            user_sett.save()
            return redirect('board:user_settings')
    else:
        form = PreferencesForm(instance=pref)
    return render(request, 'board/user_settings.html',
                  {'user_stat': user_stat, 'form': form})


def advertisement_list(request: HttpRequest, pk: int | None = None) -> HttpResponseRedirect:
    """
    Представление - Просмотр списка объявлений.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: Остаемся на странице.
    """
    context = {}
    if pk:
        advertisements = Advertisement.objects.filter(author=pk).order_by('-id')
        user_stat_ = UserStat.objects.filter(user=pk)
        context = {'user_show': User.objects.get(id=pk)}
        if user_stat_:
            context['user_stat'] = user_stat_.first()
    else:
        advertisements = Advertisement.objects.all().order_by('-id')
    page_count = read_pade_count(request)
    paginator = Paginator(advertisements, page_count)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    images = []
    for adv in range(len(page_obj)):
        images.append(Image.objects.filter(advertisement=page_obj[adv].id))
    context = {**context, 'advertisements': zip(page_obj, images), 'advertisements_feeds': page_obj}
    return render(request, 'board/advertisement_list.html', context)


def advertisement_detail(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Представление - Просмотр выбранного объявления.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: В случае нажатия кнопки Редактировать - переходим на страницу редактирования объявления.
    """
    advertisement = Advertisement.objects.get(pk=pk)
    images = Image.objects.filter(advertisement=advertisement.id)
    comments = Comment.objects.filter(advertisement=advertisement.id)
    context = like_read(request, pk)
    return render(request, 'board/advertisement_detail.html',
                  {'advertisement': advertisement,
                   'images': images,
                   'comments': comments,
                   **context})


@login_required
def add_advertisement(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление - Добавить новое объявление.
    :param request: HttpRequest - запрос пользователя.
    :return: После добавления объявления, возвращаемся к списку объявлений.
    """
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def add_comment(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Представление - Добавить новый комментарий.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: После добавления комментария, возвращаемся к деталям объявления.
    """
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.advertisement = Advertisement.objects.get(id=pk)
            comment.save()
            return redirect('board:advertisement_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'board/add_comment.html', {'form': form})


@login_required
def add_image(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Представление - Добавить новые картинки.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: После добавления картинок, возвращаемся к редактированию объявления.
    """
    advertisement = Advertisement.objects.get(id=pk)
    if request.method == "POST":
        uploaded_images = request.FILES.getlist('photo')
        for image in uploaded_images:
            Image.objects.create(advertisement=advertisement, user=request.user, image=image)
        return redirect('board:edit_advertisement', pk=pk)
    else:
        form = ImageForm()
    return render(request, 'board/add_image.html',
                  {'form': form, 'advertisement': advertisement})


@login_required
def edit_advertisement(request: HttpRequest, pk) -> HttpResponseRedirect:
    """
    Представление - Редактирование выбранного объявления. Редактировать можно только
    свои объявления или суперпользователю можно редактировать все.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: После редактирования возвращаемся на страницу просмотра деталей выбранного объявления.
    """
    advertisement = Advertisement.objects.get(pk=pk)
    images = Image.objects.filter(advertisement=advertisement)
    if request.user != advertisement.author and not request.user.is_superuser:
        return render(request, 'board/advertisement_detail.html',
                      {'advertisement': advertisement, 'error': 'Вы не можете редактировать чужие объявления!'})
    if request.method == "POST" and request.POST.get('add_adv'):
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.save()
            return redirect('board:advertisement_detail', pk=pk)
    elif request.method == "POST" and request.POST.get('image_del'):
        for img in images:
            image = request.POST.get(f'i{img.id}')
            if image:
                Image.objects.get(id=img.id).delete()
        form = AdvertisementForm(instance=advertisement)
        images = Image.objects.filter(advertisement=advertisement)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/add_advertisement.html',
                  {'form': form,
                   'title2': 'Редактировать объявление',
                   'advertisement': advertisement,
                   'images': images})

@login_required
def edit_comment(request: HttpRequest, pk) -> HttpResponseRedirect:
    """
    Представление - Редактирование выбранного сомментария. Редактировать можно только
    свои комментарии или суперпользователю можно редактировать все.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id комментария.
    :return: После редактирования возвращаемся на ту же страницу.
    """
    comment = Comment.objects.get(pk=pk)
    # images = Image.objects.filter(advertisement=advertisement)
    if request.user != comment.author and not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            pk = comment.advertisement.id
            return redirect('board:advertisement_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'board/add_comment.html',
                  {'form': form,
                   'title2': 'Редактировать комментарий'})


@login_required
def image_generation(request: HttpRequest, pk) -> HttpResponse:
    """
    Представление - Генерация изображения с помощью API Kandinski 3.0
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: После редактирования возвращаемся на страницу просмотра деталей выбранного объявления.
    """
    advertisement = Advertisement.objects.get(pk=pk)
    file_name = f"img_{time.time_ns()}.jpg"
    for i in '?!:;,*$№#%@"~`()[]{}<>':
        file_name = file_name.replace(i, '')
    dir_ = os.path.join(settings.MEDIA_ROOT, f'images/kandinsky/{datetime.now().year}_{datetime.now().month}').replace("\\", "/")
    try:
        os.mkdir(dir_)
    except FileExistsError:
        print('exist')
    file = os.path.join(dir_, file_name).replace("\\", "/")
    file_name_cut = '/'.join(file.split('/')[-4:])

    Image.objects.create(advertisement=advertisement, user=request.user, image=file_name_cut)
    shutil.copy(os.path.join(settings.MEDIA_ROOT, 'gen.jpg'), dir_)
    os.rename(os.path.join(dir_, 'gen.jpg'), file)
    proc = Thread(target=kandinsky_query, args=(f'{advertisement.title} {advertisement.content}', dir_, file_name))
    proc.start()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def del_advertisement(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Представление - Удаление выбранного объявления. Удалять можно только свои объявления.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: После удаления возвращаемся на страницу списка объявления.
    """
    advertisement = Advertisement.objects.get(pk=pk)
    if request.user != advertisement.author:
        return render(request, 'board/advertisement_detail.html',
                      {'advertisement': advertisement, 'error': 'Вы не можете удалить чужие объявления!'})
    if request.method == "POST":
        Advertisement.objects.get(id=pk).delete()
        return redirect('board:advertisement_list')
    return render(request, 'board/advertisement_detail.html',
                      {'advertisement': advertisement})


@login_required
def delete_comment(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """
    Представление - Удаление выбранного комментария. Удалять можно только свои объявления
    или суперпользователю можно все.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id комментария.
    :return: После удаления возвращаемся на страницу списка объявления.
    """
    comment = Comment.objects.get(pk=pk)
    if request.user == comment.author:
        Comment.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_dislike(request: HttpRequest, pk: int, tp: int):
    """
    Поставить лайк/дизлайк объявлению.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :param tp: Тип лйка.
    :return: Посл записи лайка/дизлайка возвращаемся к странице с деталями объявления
    """
    like_set(request, pk=pk, tp=tp)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

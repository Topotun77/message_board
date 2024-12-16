from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from .models import Advertisement, Image, Comment
from .forms import AdvertisementForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """
    Представление - Выход из системы (logout)
    :param request: HttpRequest - запрос пользователя
    :return: HttpResponseRedirect - перенаправление на домашнюю страницу
    """
    logout(request)
    return redirect('home')


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


def advertisement_list(request: HttpRequest, pk: int | None = None) -> HttpResponseRedirect:
    """
    Представление - Просмотр списка объявлений.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: Остаемся на странице.
    """
    context = {}
    if pk:
        advertisements = Advertisement.objects.filter(author=pk)
        context = {'user_show': User.objects.get(id=pk)}
    else:
        advertisements = Advertisement.objects.all()
    images = []
    for adv in advertisements:
        images.append(Image.objects.filter(advertisement=adv.id))
    context = {**context, 'advertisements': zip(advertisements, images)}
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
    return render(request, 'board/advertisement_detail.html',
                  {'advertisement': advertisement, 'images': images, 'comments': comments})


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
def edit_advertisement(request: HttpRequest, pk) -> HttpResponseRedirect:
    """
    Представление - Редактирование выбранного объявления. Редактировать можно только
    свои объявления.
    :param request: HttpRequest - запрос пользователя.
    :param pk: id объявления.
    :return: После редактирования возвращаемся на страницу просмотра деталей выбранного объявления.
    """
    advertisement = Advertisement.objects.get(pk=pk)
    if request.user != advertisement.author and not request.user.is_superuser:
        return render(request, 'board/advertisement_detail.html',
                      {'advertisement': advertisement, 'error': 'Вы не можете редактировать чужие объявления!'})
    if request.method == "POST" and request.POST.get('add_adv'):
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.save()
            return redirect('board:advertisement_detail', pk=pk)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/add_advertisement.html',
                  {'form': form, 'title2': 'Редактировать объявление', 'advertisement': advertisement})


@login_required
def del_advertisement(request: HttpRequest, pk) -> HttpResponseRedirect:
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


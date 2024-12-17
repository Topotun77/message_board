from django.http import HttpRequest
from .models import Like, Advertisement


def like_read(request: HttpRequest, pk: int) -> dict:
    context = {}
    if request.user.is_authenticated:
        if Like.objects.filter(advertisement=pk, user=request.user.id, like_type=1):
            context['like'] = 1
        elif Like.objects.filter(advertisement=pk, user=request.user.id, like_type=0):
            context['dislike'] = 1
    return context


def like_set(request: HttpRequest, pk: int, tp: int):
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

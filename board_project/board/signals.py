from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Advertisement, Like, UserStat


@receiver(post_save, sender=Advertisement)
@receiver(post_delete, sender=Advertisement)
def create_notification_for_partner(sender, instance, created='delete', **kwargs):
    if created:
        count_avg = len(sender.objects.filter(author=instance.author))
        avg = UserStat.objects.get(user=instance.author)
        if avg:
            avg.advertisement_count = count_avg
            avg.save()
        else:
            UserStat.objects.create(user=instance.author, advertisement_count=count_avg)


@receiver(post_save, sender=Like)
@receiver(post_delete, sender=Like)
def create_notification_for_partner(sender, instance, created='delete', **kwargs):
    if created:
        count_like = len(sender.objects.filter(user=instance.user, like_type=1))
        count_dislike = len(sender.objects.filter(user=instance.user, like_type=0))
        avg = UserStat.objects.get(user=instance.user)
        if avg:
            avg.like_count = count_like
            avg.dislike_count = count_dislike
            avg.save()
        else:
            UserStat.objects.create(user=instance.user, like_count=count_like, dislike_count=count_dislike)

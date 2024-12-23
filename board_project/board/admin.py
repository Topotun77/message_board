from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Advertisement, Comment, Preferences, Image, Like, UserStat

# admin.site.register(Advertisement)
admin.site.register(Comment)
admin.site.register(Preferences)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(UserStat)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    readonly_fields = ['preview']
    list_display = ('title', 'content', 'author', 'image', 'like_count', 'dislike_count', 'created_at')
    fieldsets = (
        ('Description', {
            'fields': ('title',
                       'content',
                       'author')
        }),
        ('Parameters', {
            'fields': (('like_count', 'dislike_count'),
                       ('image', 'preview'),)
        })
    )
    search_fields = ('title', 'content', 'author')
    list_filter = ('title', 'content', 'author')

    def preview(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' height='300'>")

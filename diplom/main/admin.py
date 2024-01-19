from django.contrib import admin
from . models import *
from ..common.admin import BaseAdmin


class PetitionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description'] + BaseAdmin.list_display
    list_filter = ['user', 'title', 'description']
    search_fields = ['user', 'title', 'description']


class LikesAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition'] + BaseAdmin.list_display
    list_filter = ['user', 'petition']
    search_fields = ['user', 'petition']


class DislikesAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition'] + BaseAdmin.list_display
    list_filter = ['user', 'petition']
    search_fields = ['user', 'petition']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'text'] + BaseAdmin.list_display
    list_filter = ['user', 'petition', 'text']
    search_fields = ['user', 'petition', 'text']


admin.site.register(Petition, PetitionAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(Dislikes, DislikesAdmin)
admin.site.register(Comment, CommentAdmin)

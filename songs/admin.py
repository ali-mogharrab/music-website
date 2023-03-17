from django.contrib import admin

from .models import Artist, Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['profile', 'nickname', 'created']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

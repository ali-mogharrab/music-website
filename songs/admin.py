from django.contrib import admin

from .models import Album, Artist, Review, Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['profile', 'nickname', 'created']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['song', 'owner', 'value']
    list_filter = ('value', )

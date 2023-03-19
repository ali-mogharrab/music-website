from django import forms

from .models import Song, Album


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['album', 'name']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name']

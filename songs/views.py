from django.shortcuts import render
from django.views import View

from .models import Artist, Song


class Index(View):
    def get(self, request):
        context = {}
        return render(request, 'songs/index.html', context=context)


class Songs(View):
    def get(self, request):
        songs = Song.objects.all()
        context = {'songs': songs}
        return render(request, 'songs/songs.html', context=context)


class Artists(View):
    def get(self, request):
        artists = Artist.objects.all()
        context = {'artists': artists}
        return render(request, 'songs/artists.html', context=context)


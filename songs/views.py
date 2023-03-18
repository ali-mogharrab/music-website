from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import SongForm
from .models import Album, Artist, Song


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


class GetArtist(View):
    def get(self, request, pk):
        artist = Artist.objects.get(id=pk)
        context = {'artist': artist}
        return render(request, 'songs/artist.html', context=context)


class Albums(View):
    def get(self, request):
        albums = Album.objects.all()
        context = {'albums': albums}
        return render(request, 'songs/albums.html', context=context)


class GetAlbum(View):
    def get(self, request, pk):
        album = Album.objects.get(id=pk)
        context = {'album': album}
        return render(request, 'songs/album.html', context=context)


class CreateSong(View):
    def get(self, request):
        form = SongForm()
        context = {'form': form}
        return render(request, 'songs/create_song.html', context=context)
    
    def post(self, request):
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user.profile.artist
            song.save()
            return redirect('songs')
        
        else:
            messages.error(request, 'An error occurred during creating song')
            return redirect('create_song')

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import AlbumForm, SongForm
from .models import Album, Artist, Song
from .utils import Search


class Index(View):
    def get(self, request):
        search = Search(request)
        result_objects, search_query = search()

        context = {'objects': result_objects, 'search_query': search_query}
        return render(request, 'songs/index.html', context=context)


class Songs(View):
    def get(self, request):
        songs = Song.objects.all()
        context = {'songs': songs}
        return render(request, 'songs/songs.html', context=context)


class GetSong(View):
    def get(self, request, pk):
        song = Song.objects.get(id=pk)
        context = {'song': song}
        return render(request, 'songs/song.html', context=context)


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


class CreateAlbum(View):
    def get(self, request):
        form = AlbumForm()
        context = {'form': form}
        return render(request, 'songs/create_album.html', context=context)

    def post(self, request):
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            try:
                artist = request.user.profile.artist
            except:
                return redirect('index')

            album = form.save()
            album.artist.add(artist)
            album.save()
            return redirect('albums')

        else:
            messages.error(request, 'An error occurred during creating album')
            return redirect('create_album')


class CreateSong(View):
    def get(self, request):
        try:
            artist = request.user.profile.artist
        except:
            return redirect('index')

        album = artist.album_set.all()

        form = SongForm(albums=album)
        context = {'form': form}
        return render(request, 'songs/create_song.html', context=context)

    def post(self, request):
        try:
            artist = request.user.profile.artist
        except:
            return redirect('index')

        album = artist.album_set.all()

        form = SongForm(request.POST, request.FILES, albums=album)
        if form.is_valid():
            song = form.save()
            song.artist.add(artist)
            song.save()
            return redirect('songs')

        else:
            messages.error(request, 'An error occurred during creating song')
            return redirect('create_song')

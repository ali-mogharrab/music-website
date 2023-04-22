from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import AlbumForm, ReviewForm, SongForm
from .models import Album, Artist, Song
from .utils import Search, paginate_objects


class Index(View):
    def get(self, request):
        search = Search(request)
        result_objects, search_query = search()

        objects, custom_range = paginate_objects(request, result_objects, 8)

        context = {'objects': objects, 'search_query': search_query, 'custom_range': custom_range}
        return render(request, 'songs/index.html', context=context)


class Songs(View):
    def get(self, request):
        songs = Song.objects.all()

        songs, custom_range = paginate_objects(request, songs, 8)

        context = {'songs': songs, 'custom_range': custom_range}
        return render(request, 'songs/songs.html', context=context)


class GetSong(View):
    def get(self, request, pk):
        song = Song.objects.get(id=pk)
        form = ReviewForm()
        context = {'song': song, 'form': form}
        return render(request, 'songs/song.html', context=context)

    def post(self, request, pk):
        song = Song.objects.get(id=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.song = song
            review.owner = request.user.profile
            review.save()

            song.set_vote_count

            messages.success(request, 'Vote added successfully')

        else:
            messages.error(request, 'An error occurred during adding vote')

        return redirect('song', pk=pk)


class MySongs(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            artist = request.user.profile.artist
        except:
            return redirect('songs')

        songs = artist.song_set.all()
        context = {'songs': songs}
        return render(request, 'songs/my_songs.html', context=context)


class UpdateSong(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        try:
            artist = request.user.profile.artist
        except:
            return redirect('index')

        albums = artist.album_set.all()

        song = Song.objects.get(id=pk)

        form = SongForm(albums=albums, instance=song)

        context = {'form': form, 'song': song}
        return render(request, 'songs/update_song.html', context=context)

    def post(self, request, pk):
        try:
            artist = request.user.profile.artist
        except:
            return redirect('index')

        albums = artist.album_set.all()

        song = Song.objects.get(id=pk)

        form = SongForm(request.POST, request.FILES, albums=albums, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, 'Song updated successfully')
            return redirect('my_songs')

        else:
            messages.error(request, 'An error occurred during updating song')
            return redirect('my_songs')


class DeleteSong(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        song = Song.objects.get(id=pk)
        context = {'song': song}
        return render(request, 'songs/delete_song.html', context=context)

    def post(self, request, pk):
        song = Song.objects.get(id=pk)
        if request.POST.get('delete') == 'Yes':
            song.delete()
            messages.success(request, 'Song deleted successfully')

        return redirect('my_songs')


class Artists(View):
    def get(self, request):
        artists = Artist.objects.all()

        artists, custom_range = paginate_objects(request, artists, 8)

        context = {'artists': artists, 'custom_range': custom_range}
        return render(request, 'songs/artists.html', context=context)


class GetArtist(View):
    def get(self, request, pk):
        artist = Artist.objects.get(id=pk)

        songs = Song.objects.filter(artist=artist)

        albums = Album.objects.filter(artist=artist)

        context = {'artist': artist, 'songs': songs, 'albums': albums}
        return render(request, 'songs/artist.html', context=context)


class Albums(View):
    def get(self, request):
        albums = Album.objects.all()

        albums, custom_range = paginate_objects(request, albums, 8)

        context = {'albums': albums, 'custom_range': custom_range}
        return render(request, 'songs/albums.html', context=context)


class GetAlbum(View):
    def get(self, request, pk):
        album = Album.objects.get(id=pk)

        songs = album.song_set.all()

        artists = album.artist.all()

        context = {'album': album, 'songs': songs, 'artists': artists}
        return render(request, 'songs/album.html', context=context)


class MyAlbums(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        try:
            artist = request.user.profile.artist
        except:
            return render('albums')

        albums = artist.album_set.all()
        context = {'albums': albums}
        return render(request, 'songs/my_albums.html', context=context)


class UpdateAlbum(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        album = Album.objects.get(id=pk)
        form = AlbumForm(instance=album)
        context= {'form': form, 'album': album}
        return render(request, 'songs/update_album.html', context=context)

    def post(self, request, pk):

        album = Album.objects.get(id=pk)

        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Album updated successfully')
            return redirect('my_albums')

        else:
            messages.error(request, 'An error occurred during updating Album')
            return redirect('my_albums')


class DeleteAlbum(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        album = Album.objects.get(id=pk)
        context = {'album': album}
        return render(request, 'songs/delete_album.html', context=context)

    def post(self, request, pk):
        album = Album.objects.get(id=pk)
        if request.POST.get('delete') == 'Yes':
            album.delete()
            messages.success(request, 'Album deleted successfully')

        return redirect('my_albums')


class CreateAlbum(LoginRequiredMixin, View):
    login_url = 'login'

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
                messages.error(request, 'An error occurred during creating album')
                return redirect('index')

            album = form.save()
            album.artist.add(artist)
            album.save()
            return redirect('albums')

        else:
            messages.error(request, 'An error occurred during creating album')
            return redirect('create_album')


class CreateSong(LoginRequiredMixin, View):
    login_url = 'login'

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
            messages.success(request, 'Song created successfully')
            return redirect('songs')

        else:
            messages.error(request, 'An error occurred during creating song')
            return redirect('create_song')

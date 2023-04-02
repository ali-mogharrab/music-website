from itertools import chain

from django.db.models import Q

from .models import Album, Artist, Song


class Search:
    def __init__(self, request):
        self.search_query = ''
        self.search_part = 'all'

        if request.GET.get('search_query'):
            self.search_query = request.GET.get('search_query')
            self.search_part = request.GET.get('search_part')

    def search_songs(self):
        artists = Artist.objects.filter(nickname__icontains=self.search_query)

        songs = Song.objects.filter(
            Q(name__icontains=self.search_query) |
            Q(album__name__icontains=self.search_query) |
            Q(artist__in=artists)
        )
        return songs

    def search_artists(self):
        artists = Artist.objects.filter(nickname__icontains=self.search_query)
        return artists

    def search_albums(self):
        albums = Album.objects.filter(name__icontains=self.search_query)
        return albums

    def __call__(self):
        result_objects = list()

        if self.search_part == 'all':
            songs = self.search_songs()
            artists = self.search_artists()
            albums = self.search_albums()
            result_objects = list(chain(songs, artists, albums))

        elif self.search_part == 'songs':
            songs = self.search_songs()
            result_objects = songs

        elif self.search_part == 'artists':
            artists = self.search_artists()
            result_objects = artists

        elif self.search_part == 'albums':
            albums = self.search_albums()
            result_objects = albums

        return result_objects, self.search_query

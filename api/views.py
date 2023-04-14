from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from songs.models import Song

from .serializers import SongSerializer


class Logout(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'User loged out successfully'})


class Songs(APIView):

    def get(self, request):
        songs = Song.objects.all()
        song_serializer = SongSerializer(instance=songs, many=True)
        return Response(data=song_serializer.data)

    def post(self, request):
        song_serializer = SongSerializer(data=request.data)
        if song_serializer.is_valid():
            song_serializer.save()
            return Response(data={'message': 'Song added successfully'}, status=status.HTTP_201_CREATED)

        return Response(data=song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSong(APIView):
    permission_classes = (IsAuthenticated, )

    def get_song(self, pk):
        try:
            song = Song.objects.get(id=pk)
            return song
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        song = self.get_song(pk)
        song_serializer = SongSerializer(instance=song)
        return Response(data=song_serializer.data)

    def put(self, request, pk):
        song = self.get_song(pk)
        song_serializer = SongSerializer(instance=song, data=request.data, partial=True)
        if song_serializer.is_valid():
            song_serializer.save()
            return Response(song_serializer.data)
        return Response(song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        song = self.get_song(pk)
        song.delete()
        return Response(data={'message': 'song deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

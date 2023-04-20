from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Message, Profile
from songs.models import Album, Artist, Review, Song

from .permissions import IsArtist, IsArtistOrReadOnly, IsProfile, IsUser
from .serializers import (AlbumSerializer, ArtistSerializer, MessageSerializer,
                          ProfileSerializer, ReviewSerializer, SongSerializer,
                          UserSerializer)


class Logout(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'User loged out successfully'})

# ////////////////////////////////////////////////////////////

class Users(APIView):

    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(instance=users, many=True)
        return Response(data=user_serializer.data)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            message = {
                'message': 'User created successfully',
                'id': user.id,
                # send PUT request because profile has been created by profiles/signals.py
                'send PUT request to update profile': f"{request.META['HTTP_HOST']}/api/profile/{user.profile.id}/",
            }
            return Response(data=message, status=status.HTTP_201_CREATED)

        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    permission_classes = (IsAuthenticated, IsUser)

    def get_user(self, pk):
        try:
            user = User.objects.get(id=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_user(pk)
        self.check_object_permissions(request, user)
        user_serializer = UserSerializer(instance=user)
        return Response(data=user_serializer.data)

    def put(self, request, pk):
        user = self.get_user(pk)
        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data)

        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user(pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(data={'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# ////////////////////////////////////////////////////////////

class Profiles(APIView):

    def get(self, request):
        profiles = Profile.objects.all()
        profile_serializer = ProfileSerializer(instance=profiles, many=True)
        return Response(data=profile_serializer.data)


class GetProfile(APIView):
    permission_classes = (IsAuthenticated, IsProfile)

    def get_profile(self, pk):
        try:
            profile = Profile.objects.get(id=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_profile(pk)
        self.check_object_permissions(request, profile)
        profile_serializer = ProfileSerializer(instance=profile)
        return Response(data=profile_serializer.data)

    def put(self, request, pk):
        profile = self.get_profile(pk)
        self.check_object_permissions(request, profile)

        profile_serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile = profile_serializer.save()

            if profile.is_artist:
                message = {
                    'message': 'Profile updated successfully',
                    'id': profile.id,
                    # send PUT request because artist has been created by profiles/signals.py
                    'send PUT request to update artist': f"{request.META['HTTP_HOST']}/api/artist/{profile.artist.id}/",
                }
            else:
                message = profile_serializer.data

            return Response(data=message)

        return Response(data=profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ////////////////////////////////////////////////////////////

class Artists(APIView):

    def get(self, request):
        artists = Artist.objects.all()
        artist_serailizer = ArtistSerializer(instance=artists, many=True)
        return Response(data=artist_serailizer.data)


class GetArtist(APIView):
    permission_classes = (IsAuthenticated, IsArtist)

    def get_artist(self, pk):
        try:
            artist = Artist.objects.get(id=pk)
            return artist
        except Artist.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        artist = self.get_artist(pk)
        self.check_object_permissions(request, artist)
        artist_serializer = ArtistSerializer(instance=artist)
        return Response(data=artist_serializer.data)

    def put(self, request, pk):
        artist = self.get_artist(pk)
        self.check_object_permissions(request, artist)

        artist_serializer = ArtistSerializer(instance=artist, data=request.data, partial=True)
        if artist_serializer.is_valid():
            artist_serializer.save()
            return Response(data=artist_serializer.data)

        return Response(data=artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ////////////////////////////////////////////////////////////

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
    permission_classes = (IsAuthenticated, IsArtistOrReadOnly)

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
        self.check_object_permissions(request, song)

        song_serializer = SongSerializer(instance=song, data=request.data, partial=True)
        if song_serializer.is_valid():
            song_serializer.save()
            return Response(data=song_serializer.data)

        return Response(data=song_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        song = self.get_song(pk)
        self.check_object_permissions(request, song)
        song.delete()
        return Response(data={'message': 'Song deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# ////////////////////////////////////////////////////////////

class Albums(APIView):

    def get(self, request):
        albums = Album.objects.all()
        album_serializer = AlbumSerializer(instance=albums, many=True)
        return Response(data=album_serializer.data)

    def post(self, request):
        album_serializer = AlbumSerializer(data=request.data)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(data={'message': 'Album created successfully'}, status=status.HTTP_201_CREATED)

        return Response(data=album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAlbum(APIView):
    permission_classes = (IsAuthenticated, IsArtistOrReadOnly)

    def get_album(self, pk):
        try:
            album = Album.objects.get(id=pk)
            return album
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        album = self.get_album(pk)
        album_serializer = AlbumSerializer(instance=album)
        return Response(data=album_serializer.data)

    def put(self, request, pk):
        album = self.get_album(pk)
        self.check_object_permissions(request, album)

        album_serializer = AlbumSerializer(instance=album, data=request.data, partial=True)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(data=album_serializer.data)

        return Response(data=album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        album = self.get_album(pk)
        self.check_object_permissions(request, album)
        album.delete()
        return Response(data={'message': 'Album deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# ////////////////////////////////////////////////////////////

class Messages(APIView):

    def get(self, request):
        messages = Message.objects.all()
        message_serializer = MessageSerializer(instance=messages, many=True)
        return Response(data=message_serializer.data)

    def post(self, request):
        message_serializer = MessageSerializer(data=request.data)
        if message_serializer.is_valid():
            message_serializer.save()
            return Response(data={'message': 'Message created successfully'}, status=status.HTTP_201_CREATED)

        return Response(data=message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMessage(APIView):
    permission_classes = (IsAuthenticated, IsProfile)

    def get_message(self, pk):
        try:
            message = Message.objects.get(id=pk)
            return message
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        message = self.get_message(pk)
        message_serializer = MessageSerializer(instance=message)
        return Response(data=message_serializer.data)

    def put(self, request, pk):
        message = self.get_message(pk)
        self.check_object_permissions(request, obj=message.sender)

        message_serializer = MessageSerializer(instance=message, data=request.data, partial=True)
        if message_serializer.is_valid():
            message_serializer.save()
            return Response(data=message_serializer.data)

        return Response(data=message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = self.get_message(pk)
        self.check_object_permissions(request, obj=message.sender)
        message.delete()
        return Response(data='Message deleted successfully', status=status.HTTP_204_NO_CONTENT)

# ////////////////////////////////////////////////////////////

class Reviews(APIView):

    def get(self, request):
        reviews = Review.objects.all()
        review_serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(data=review_serializer.data)

    def post(self, request):
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(data={'message': 'Review created successfully'}, status=status.HTTP_201_CREATED)

        return Response(data=review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetReview(APIView):
    permission_classes = (IsAuthenticated, IsProfile)

    def get_review(self, pk):
        try:
            review = Review.objects.get(id=pk)
            return review
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        review = self.get_review(pk)
        review_serializer = ReviewSerializer(instance=review)
        return Response(data=review_serializer.data)

    def put(self, request, pk):
        review = self.get_review(pk)
        self.check_object_permissions(request, obj=review.owner)

        review_serializer = ReviewSerializer(instance=review, data=request.data, partial=True)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(data=review_serializer.data)

        return Response(data=review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_review(pk)
        self.check_object_permissions(request, obj=review.owner)
        review.delete()
        return Response(data={'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

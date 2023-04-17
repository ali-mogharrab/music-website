from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from songs.models import Song

from .permissions import IsArtistOrReadOnly, IsProfile, IsUser
from .serializers import ProfileSerializer, SongSerializer, UserSerializer


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

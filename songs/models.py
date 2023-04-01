import uuid

from django.db import models

from profiles.models import Profile


class Artist(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='artist_images', default='defaults/default_profile.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.nickname)


class Album(models.Model):
    artist = models.ManyToManyField(Artist, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='album_covers', default='defaults/default_album.jpg')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Song(models.Model):
    artist = models.ManyToManyField(Artist, blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='song_covers', default='defaults/default_song.jpg')
    song_file = models.FileField(null=True, blank=True, upload_to='song_files')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

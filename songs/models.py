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
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'name']

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set

    @property
    def set_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        ratio = (up_votes / total_votes) * 100

        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up  vote'),
        ('down', 'Down vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=VOTE_TYPE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'song']]

    def __str__(self):
        return self.value

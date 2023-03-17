import uuid

from django.db import models

from profiles.models import Profile


class Artist(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

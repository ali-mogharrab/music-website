from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from songs.models import Artist


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
        )

def create_artist(sender, instance, created, **kwargs):
    if created:
        profile = instance
        Artist.objects.create(
            profile=profile,
        )


post_save.connect(create_profile, sender=User)
post_save.connect(create_artist, sender=Profile)

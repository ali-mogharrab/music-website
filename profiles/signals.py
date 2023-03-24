from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save

from songs.models import Artist

from .models import Profile


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

        subject = 'Welcom to music website'
        message = 'We are glad you are here!'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[profile.user.email],
            fail_silently=False,
        )


post_save.connect(create_profile, sender=User)
post_save.connect(create_artist, sender=Profile)

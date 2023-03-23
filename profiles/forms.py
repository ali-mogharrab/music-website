from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from songs.models import Artist

from .models import Message, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'phone', 'is_artist']


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['nickname', 'bio']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['email', 'subject', 'body']

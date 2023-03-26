from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from songs.models import Artist

from .models import Message, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'phone', 'is_artist']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            print('*'*40, field.widget.attrs)
            field.widget.attrs.update({'class': 'input'})



class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['nickname', 'bio']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            if name == 'body':
                field.widget.attrs.update({'class': 'message_input'})
            else:
                field.widget.attrs.update({'class': 'input'})

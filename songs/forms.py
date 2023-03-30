from django import forms

from .models import Album, Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['album', 'name', 'image']

    album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        albums = kwargs.pop('albums', None)
        super().__init__(*args, **kwargs)
        self.fields['album'].queryset = albums

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'image']

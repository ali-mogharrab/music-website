from django import forms

from .models import Album, Review, Song


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['album', 'name', 'image', 'song_file']

    album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        albums = kwargs.pop('albums', None)
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = albums

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

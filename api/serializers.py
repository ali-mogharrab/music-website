from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profiles.models import Message, Profile
from songs.models import Album, Artist, Song


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError({'password': "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password1'])
        user.username = user.username.lower()
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        # if user sent  password to update
        if 'password1' in validated_data:
            instance.set_password(validated_data['password1'])
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'age', 'gender', 'phone', 'is_artist']

    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_artist = validated_data.get('is_artist', instance.is_artist)
        instance.save()
        return instance


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'nickname', 'bio']

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance

# ////////////////////////////////////////////////////////////

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['name', 'album', 'artist']

    def create(self, validated_data):
        artist = validated_data.pop('artist', None)
        song = Song.objects.create(**validated_data)
        # artist is many to many field
        song.artist.set(artist)
        song.save()
        return song

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.album = validated_data.get('album', instance.album)
        instance.artist.set(validated_data.get('artist', instance.artist))
        instance.save()
        return instance

# ////////////////////////////////////////////////////////////

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'artist']

    def create(self, validated_data):
        artist = validated_data.pop('artist', None)
        album = Album.objects.create(**validated_data)
        # artist is many to many field
        album.artist.set(artist)
        album.save()
        return album

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.artist.set(validated_data.get('artist', instance.artist))
        instance.save()
        return instance

# ////////////////////////////////////////////////////////////

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'email', 'subject', 'body', 'is_read']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message

    def update(self, instance, validated_data):
        instance.sender = validated_data.get('sender', instance.sender)
        instance.email = validated_data.get('email', instance.email)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.body = validated_data.get('body', instance.body)
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance

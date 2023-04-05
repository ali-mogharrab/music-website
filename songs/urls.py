from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('songs/', views.Songs.as_view(), name='songs'),
    path('song/<str:pk>/', views.GetSong.as_view(), name='song'),
    path('artists/', views.Artists.as_view(), name='artists'),
    path('artist/<str:pk>/', views.GetArtist.as_view(), name='artist'),
    path('albums/', views.Albums.as_view(), name='albums'),
    path('album/<str:pk>/', views.GetAlbum.as_view(), name='album'),
    path('create_album/', views.CreateAlbum.as_view(), name='create_album'),
    path('create_song/',  views.CreateSong.as_view(), name='create_song'),
    path('my_songs/', views.MySongs.as_view(), name='my_songs'),
    path('update_song/<str:pk>/', views.UpdateSong.as_view(), name='update_song'),
    path('my_albums/', views.MyAlbums.as_view(), name='my_albums'),
    path('update_album/<str:pk>/', views.UpdateAlbum.as_view(), name='update_album'),
]

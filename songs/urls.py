from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('songs/', views.Songs.as_view(), name='songs'),
    path('artists/', views.Artists.as_view(), name='artists'),
    path('artist/<str:pk>/', views.GetArtist.as_view(), name='artist'),
    path('albums/', views.Albums.as_view(), name='albums'),
    path('album/<str:pk>/', views.GetAlbum.as_view(), name='album'),
    path('create_song/',  views.CreateSong.as_view(), name='create_song'),
]

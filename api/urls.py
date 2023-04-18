from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', view=obtain_auth_token, name='api-login'),
    path('logout/', views.Logout.as_view(), name='api-logout'),
    path('users/', views.Users.as_view(), name='api-users'),
    path('user/<str:pk>/', views.GetUser.as_view(), name='api-user'),
    path('profiles/', views.Profiles.as_view(), name='api-profiles'),
    path('profile/<str:pk>/', views.GetProfile.as_view(), name='api-profile'),
    path('artists/', views.Artists.as_view(), name='api-artists'),
    path('artist/<str:pk>/', views.GetArtist.as_view(), name='api-artist'),
    path('songs/', views.Songs.as_view(), name='api-songs'),
    path('song/<str:pk>/', views.GetSong.as_view(), name='api-song'),
    path('albums/', views.Albums.as_view(), name='api-albums'),
    path('album/<str:pk>/', views.GetAlbum.as_view(), name='api-album'),
]
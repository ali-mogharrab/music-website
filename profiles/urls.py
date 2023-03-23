from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('edit_profile/', views.EditProfile.as_view(), name='edit_profile'),
    path('edit_artist/', views.EditArtist.as_view(), name='edit_artist'),
    path('contact/', views.Contact.as_view(), name='contact'),
]

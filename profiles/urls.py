from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('edit-profile/', views.EditProfile.as_view(), name='edit-profile'),
    
]
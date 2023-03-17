from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('songs/', views.Songs.as_view(), name='songs'),
]

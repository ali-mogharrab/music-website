from django.contrib import admin

from .models import Message, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'created', 'is_artist']
    list_editable = ['is_artist']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'subject', 'created', 'is_read']
    list_editable = ['is_read']
    list_filter = ['is_read']

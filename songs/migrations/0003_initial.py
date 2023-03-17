# Generated by Django 4.1 on 2023-03-17 14:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_profile_is_artist'),
        ('songs', '0002_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]
# Generated by Django 4.1 on 2023-03-16 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('age', models.IntegerField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], max_length=1, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

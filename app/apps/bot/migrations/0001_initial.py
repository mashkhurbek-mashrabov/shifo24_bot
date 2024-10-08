# Generated by Django 5.1 on 2024-08-28 14:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('chat_id', models.CharField(max_length=40, unique=True, verbose_name='Chat ID')),
                ('name', models.CharField(max_length=40, null=True, verbose_name='Name')),
                ('username', models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='Username')),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone number')),
                ('language', models.CharField(choices=[('uz', 'Uzbek 🇺🇿'), ('en', 'English 🇬🇧'), ('ru', 'Russian 🇷🇺')], default='uz', max_length=3, verbose_name='Language')),
                ('step', models.SmallIntegerField(choices=[(1, 'Listing language'), (2, 'Edit language'), (3, 'Main menu')], default=1, verbose_name='Step')),
                ('data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]

# Generated by Django 5.1 on 2024-08-28 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Telegram id'),
        ),
    ]

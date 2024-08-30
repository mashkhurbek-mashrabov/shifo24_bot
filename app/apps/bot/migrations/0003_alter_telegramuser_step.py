# Generated by Django 5.1 on 2024-08-30 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_telegramuser_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='step',
            field=models.SmallIntegerField(choices=[(1, 'Listing language'), (2, 'Edit language'), (3, 'Main menu'), (4, 'Get phone number'), (5, 'Edit phone number'), (6, 'Settings')], default=1, verbose_name='Step'),
        ),
    ]

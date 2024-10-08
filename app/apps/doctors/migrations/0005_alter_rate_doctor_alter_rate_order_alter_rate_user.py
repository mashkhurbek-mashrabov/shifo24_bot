# Generated by Django 5.1 on 2024-08-30 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_telegramuser_step'),
        ('doctors', '0004_rate'),
        ('order', '0004_alter_order_scheduled_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='doctor',
            field=models.ForeignKey(limit_choices_to={'status': 'Active'}, on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='doctors.doctor', verbose_name='Doctor'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='order',
            field=models.ForeignKey(limit_choices_to={'status': 'completed'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rates', to='order.order', verbose_name='Queue'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rates', to='bot.telegramuser', verbose_name='User'),
        ),
    ]

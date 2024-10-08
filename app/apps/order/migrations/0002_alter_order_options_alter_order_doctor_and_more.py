# Generated by Django 5.1 on 2024-08-29 16:14

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_rename_specialization_doctor_specializations'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['scheduled_date'], 'verbose_name': 'Queue', 'verbose_name_plural': 'Queues'},
        ),
        migrations.AlterField(
            model_name='order',
            name='doctor',
            field=models.ForeignKey(limit_choices_to={'status': 'Active'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='doctors.doctor', verbose_name='Doctor'),
        ),
        migrations.AlterField(
            model_name='order',
            name='scheduled_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2024, 8, 29, 21, 14, 28, 232647))], verbose_name='Scheduled date'),
        ),
    ]

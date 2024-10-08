# Generated by Django 5.1 on 2024-08-28 12:55

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last name')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='doctors/photo/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])], verbose_name='Photo')),
                ('photo_telegram_id', models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Photo telegram id')),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone number')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('lng', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('lunch_start_time', models.TimeField(blank=True, null=True, verbose_name='Lunch start time')),
                ('lunch_end_time', models.TimeField(blank=True, null=True, verbose_name='Lunch end time')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Rejected', 'Rejected')], default='Pending', max_length=10, verbose_name='Status')),
                ('bio', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='Bio')),
                ('specialization', models.ManyToManyField(blank=True, limit_choices_to={'children__isnull': True, 'is_active': True}, related_name='doctors', to='common.specialization', verbose_name='Specializations')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], max_length=3, verbose_name='Day')),
                ('start_time', models.TimeField(verbose_name='Start time')),
                ('end_time', models.TimeField(verbose_name='End time')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_schedules', to='doctors.doctor')),
            ],
            options={
                'verbose_name': 'Work schedule',
                'verbose_name_plural': 'Work schedules',
                'unique_together': {('doctor', 'day')},
            },
        ),
    ]

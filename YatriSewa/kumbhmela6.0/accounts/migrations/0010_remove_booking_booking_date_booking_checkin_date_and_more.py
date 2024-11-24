# Generated by Django 5.1.1 on 2024-10-12 15:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_accommodation_availability_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booking_date',
        ),
        migrations.AddField(
            model_name='booking',
            name='checkin_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='booking',
            name='checkout_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='booking',
            name='guests',
            field=models.IntegerField(default=1),
        ),
    ]

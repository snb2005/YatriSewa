# Generated by Django 5.1.1 on 2024-11-13 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_emergencyannouncement_lostfounditem_sosrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sosrequest',
            name='location',
            field=models.CharField(max_length=255),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-20 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_timeslot_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='status',
        ),
    ]

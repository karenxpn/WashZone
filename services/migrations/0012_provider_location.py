# Generated by Django 5.1.3 on 2024-12-10 13:02

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_alter_service_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]

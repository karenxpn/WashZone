# Generated by Django 5.1.3 on 2024-12-06 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_servicefeature_description_servicefeature_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicefeature',
            name='description',
        ),
        migrations.RemoveField(
            model_name='servicefeature',
            name='name',
        ),
    ]
# Generated by Django 5.1.3 on 2025-01-03 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_provider_timezone_specialclosure_workinghour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='timezone',
        ),
    ]
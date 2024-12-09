# Generated by Django 5.1.3 on 2024-12-08 22:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_remove_servicefeature_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='providers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

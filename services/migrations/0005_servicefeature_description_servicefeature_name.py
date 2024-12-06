# Generated by Django 5.1.3 on 2024-12-06 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_rename_extra_cost_feature_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicefeature',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servicefeature',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-19 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_service_description_order_service_duration_and_more'),
        ('services', '0002_provider_timezone_specialclosure_workinghour'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slots', to='services.provider')),
            ],
        ),
    ]
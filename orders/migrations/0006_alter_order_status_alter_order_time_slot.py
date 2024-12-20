# Generated by Django 5.1.3 on 2024-12-20 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_time_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('time_confirmation', 'Time Confirmation'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_slot',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.timeslot'),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-05 18:09

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('extra_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('rating', models.FloatField(default=0, help_text='Rating from 0 to 5', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('number_of_reviews', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='providers', to='services.category')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('base_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('duration_in_minutes', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.provider')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_included', models.BooleanField(default=False)),
                ('extra_cost', models.DecimalField(decimal_places=2, default=0, help_text="Extra cost for the feature if it's optional", max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.feature')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='services.service')),
            ],
            options={
                'unique_together': {('service', 'feature')},
            },
        ),
    ]

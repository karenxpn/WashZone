import json
from typing import MutableMapping

from rest_framework import serializers
import ast
from WashZone.location_validation import validate_location
from services.models import Provider
from django.contrib.gis.geos import Point

from services.serializers.special_closure_serializer import SpecialClosureSerializer
from services.serializers.working_hours_serializer import WorkingHourSerializer
from services.service_models.provider import WorkingHour, SpecialClosure


class ProviderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    working_hours = WorkingHourSerializer(many=True, read_only=True)
    special_closures = SpecialClosureSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        exclude = ['location']
        extra_kwargs = {
            'email': {'required': False},
        }

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

    def get_distance(self, obj):
        if hasattr(obj, 'distance') and obj.distance is not None:
            return round(obj.distance.m, 2)
        return None


class CreateProviderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)
    working_hours = WorkingHourSerializer(many=True, required=True)
    special_closures = SpecialClosureSerializer(many=True, required=False)


    class Meta:
        model = Provider
        fields = [
            'id', 'category', 'owner', 'name', 'description', 'address',
            'contact_number', 'email', 'latitude', 'longitude', 'rating', 'number_of_reviews',
            'working_hours', 'special_closures', 'image'
        ]

        read_only_fields = ['id', 'rating', 'number_of_reviews']

    def to_internal_value(self, data):
        print(data)
        return super().to_internal_value(data)


    def create(self, validated_data):
        print("Validated data:", validated_data)

        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')

        working_hours_data = validated_data.pop('working_hours', [])
        special_closures_data = validated_data.pop('special_closures', [])

        validated_data['location'] = Point(longitude, latitude)
        provider = Provider.objects.create(**validated_data)

        working_hours = [WorkingHour(provider=provider, **wh_data) for wh_data in working_hours_data]
        WorkingHour.objects.bulk_create(working_hours)

        special_closures = [SpecialClosure(provider=provider, **sc_data) for sc_data in special_closures_data]
        SpecialClosure.objects.bulk_create(special_closures)

        return provider


class ProviderUpdateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    working_hours = WorkingHourSerializer(many=True, required=False)
    special_closures = SpecialClosureSerializer(many=True, required=False)


    class Meta:
        model = Provider
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'name': {'required': False},
            'description': {'required': False},
            'address': {'required': False},
            'contact_number': {'required': False},
            'email': {'required': False},
            'rating': {'required': False},
            'number_of_reviews': {'required': False},
            'category': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'location': {'required': False},
            'working_hours': {'required': False},
            'special_closures': {'required': False},
            'image': {'required': False}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('location', None)

        return representation

    def validate(self, data):
        return validate_location(self, data)

    def update(self, instance, validated_data):
        working_hours_data = validated_data.pop('working_hours', None)
        special_closures_data = validated_data.pop('special_closures', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if working_hours_data is not None:
            for working_hour_data in working_hours_data:
                instance.working_hours.update_or_create(**working_hour_data)

        if special_closures_data is not None:
            for closure_data in special_closures_data:
                instance.special_closures.update_or_create(**closure_data)

        instance.save()
        return instance

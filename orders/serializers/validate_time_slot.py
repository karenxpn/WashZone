from django.utils.timezone import now, localtime
from rest_framework import serializers

from orders.order_models.time_slot import TimeSlot
from services.service_models.feature import ServiceFeature


def validate_time_slot(provider, service, data):
    features = data.get('features', [])
    start_time = localtime(data.get('start_time'))
    end_time = localtime(data.get('end_time'))

    if start_time <= localtime(now()):
        raise serializers.ValidationError('The start time must be in the future.')

    total_duration = service.duration_in_minutes
    for feature_data in features:
        feature = feature_data.get('feature')
        service_feature = ServiceFeature.objects.get(service=service, feature=feature)

        if service_feature and not service_feature.is_included:
            total_duration += service_feature.extra_time_in_minutes

    # validate the provided duration matches the actual duration
    requested_duration = (end_time - start_time).total_seconds() / 60
    if requested_duration != total_duration:
        raise serializers.ValidationError('The requested time slot duration does not match the service duration.')

    # validate the provided start and end hours match providers working hours
    working_hours = provider.working_hours.filter(weekday=start_time.weekday())
    valid_slot = False

    for hours in working_hours:
        working_start = start_time.replace(hour=hours.opening_time.hour, minute=hours.opening_time.minute)
        working_end = start_time.replace(hour=hours.closing_time.hour, minute=hours.closing_time.minute)

        if working_start <= start_time and end_time <= working_end:
            valid_slot = True
            break

    if not valid_slot:
        raise serializers.ValidationError('The requested time slot is outside the provider\'s working hours.')

    special_closures = provider.special_closures.filter(date=start_time.date())

    if special_closures.exists():
        raise serializers.ValidationError('The provider is closed this day.')

    overlapping_slots = TimeSlot.objects.filter(
        provider=provider,
        is_available=False,
        start_time__lt=end_time,
        end_time__gt=start_time,
    )

    if overlapping_slots.exists():
        raise serializers.ValidationError('The requested time slot is not available.')
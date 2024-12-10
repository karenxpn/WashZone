from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'phone_number',
                  'full_name',
                  'email_promotions_enabled',
                  'notifications_enabled',
                  'latitude',
                  'longitude',)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None

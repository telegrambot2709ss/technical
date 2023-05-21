from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.utils.translation import gettext_lazy as _


class ThirtyPartySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100, required=False)
    lat = serializers.FloatField(required=False)
    long = serializers.FloatField(required=False)

    def validate(self, attrs):
        filter_url = ""
        if attrs.get('lat') and attrs.get('long'):
            filter_url = f"lat={attrs.get('lat')}&lon={attrs.get('long')}"
        if attrs.get("city"):
            filter_url += f"&q={attrs.get('city')}" if filter_url else f"q={attrs.get('city')}"

        if not filter_url:
            raise ValidationError({"error": [_("lat and long or city must is required")]})

        return filter_url

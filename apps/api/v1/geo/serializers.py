from rest_framework import serializers

from apps.geo.models import Region, District, Village


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    villages = VillageSerializer(many=True, read_only=True, source="village_district")

    class Meta:
        model = District
        fields = ["id", "name", "slug", "region", "ordering", "villages"]


class RegionListSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True, source='district_region')

    class Meta:
        model = Region
        fields = ["id", "name", "slug", "ordering", "districts"]

import os
import json
import time
from django.core.management.base import BaseCommand

from apps.geo.models import Region, District, Village


class RegionDistrictVillage:
    def __init__(self):
        self.regions = []
        self.districts = []
        self.villages = []
        if os.path.exists("regions.json"):
            with open("regions.json", "r") as f:
                self.regions = json.load(f)
        if os.path.exists("districts.json"):
            with open("districts.json", "r") as f:
                self.districts = json.load(f)
        if os.path.exists("villages.json"):
            with open("villages.json", "r") as f:
                self.villages = json.load(f)

        self.region()

    def region(self):
        for i, region in enumerate(self.regions, start=1):
            reg = self._create_region(region, ordering=i)
            self.district(region=region, reg=reg)

    def district(self, region, reg):
        i = 1
        for district in self.districts:
            if district['region_id'] == region['id']:
                district_query = self._create_district(district=district, region=reg, ordering=i)
                self.village(district=district, district_query=district_query)
                i += 1

        return 1

    def village(self, district, district_query):
        i = 1
        for village in self.villages:
            if district['id'] == village['district_id']:
                self._create_village(district=district_query, village=village, ordering=i)
                i += 1

        return 1

    def _create_region(self, region, ordering):
        region = Region.objects.create(
            name={
                "name_uz": region["name_uz"],
                "name_ru": region["name_ru"],
                "name_oz": region["name_oz"],
            },
            ordering=ordering
        )
        return region

    def _create_district(self, district, region, ordering):
        district = District.objects.create(
            name={
                "name_uz": district["name_uz"],
                "name_ru": district["name_ru"],
                "name_oz": district["name_oz"],
            },
            region=region,
            ordering=ordering
        )
        return district

    def _create_village(self, village, district, ordering):
        village = Village.objects.create(
            name={
                "name_uz": village["name_uz"],
                "name_ru": village["name_ru"],
                "name_oz": village["name_oz"],
            },
            district=district,
            ordering=ordering
        )
        return village


class Command(BaseCommand):

    def add_arguments(self, parser):
        return parser.add_argument("action", type=str)

    def handle(self, *args, **options):
        action = options.get('action')

        if action == "fixtures":
            RegionDistrictVillage()

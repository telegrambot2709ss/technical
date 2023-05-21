from django.contrib import admin
from apps.geo.models import Region, District, Village

admin.site.register(Region)
admin.site.register(District)
admin.site.register(Village)

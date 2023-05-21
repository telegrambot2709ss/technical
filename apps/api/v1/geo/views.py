from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from apps.api.v1.geo import serializers
from apps.geo.models import Region, District

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = serializers.RegionListSerializer
    ordering_fields = ("ordering",)
    permission_classes = [AllowAny]

    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return cache_page(CACHE_TTL)(view)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class DistrictListView(generics.RetrieveAPIView):
    queryset = District.objects.all()

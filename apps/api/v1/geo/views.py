from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.api.v1.geo import serializers
from apps.geo.models import Region, Village, District


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = serializers.RegionListSerializer
    ordering_fields = ("ordering",)
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

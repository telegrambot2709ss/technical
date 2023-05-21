import requests
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.thirdparty import serializers


# Task 9
class ThirtyWeatherView(generics.GenericAPIView):
    serializer_class = serializers.ThirtyPartySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filter_url = serializer.validated_data
        api_key = "ae6829f2de4af3fb24b2858626a4cd4d"

        url = f'https://api.openweathermap.org/data/2.5/weather?{filter_url}&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": 'Server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

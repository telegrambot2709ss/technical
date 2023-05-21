from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.api.v1.files import serializers
from apps.files.models import File


# Task 7
class FileCreateView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = serializers.FileSerializers
    permission_classes = (IsAuthenticated,)


class FileDownloadView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = serializers.FileSerializers
    permission_classes = (IsAuthenticated,)

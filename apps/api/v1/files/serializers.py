from rest_framework import serializers

from apps.api.v1.base.validate import validate_file_size, validate_file_extension
from apps.files.models import File


class FileSerializers(serializers.ModelSerializer):
    file = serializers.FileField(
        required=True, validators=[validate_file_extension, validate_file_size]
    )

    class Meta:
        model = File
        fields = ("file",)

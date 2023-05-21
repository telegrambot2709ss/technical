from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from django.utils.translation import gettext_lazy as _

from apps.api.v1.base.validate import validate_email
from apps.users.models import Student, User


class StudentUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[
            validate_email,
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        required=False,
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    fullname = serializers.CharField(max_length=100, required=False)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "fullname", "date_joined"]

    def validate(self, attrs):
        method = self.context['request'].method
        if method == "POST":
            if not attrs.get('fullname'):
                raise ValidationError({"fullname": [_("fullname is required")]})
            if not attrs.get('email'):
                raise ValidationError({"email": [_("email is required")]})
            if not attrs.get('username'):
                raise ValidationError({"username": [_("username is required")]})
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):
    user = StudentUserSerializer(required=True)
    university = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = Student
        fields = ["pk", "user", "status", "university", "contract"]

    def validate(self, attrs):
        method = self.context['request'].method
        if method == "POST":
            if not attrs.get('university'):
                raise ValidationError({"university": [_("university is required")]})
            if not attrs.get('contract'):
                raise ValidationError({"contract": [_("contract is required")]})
        if attrs.get('contract') and attrs['contract'] < 0:
            raise ValidationError(_("Student's counter must be greater than zero"))

        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

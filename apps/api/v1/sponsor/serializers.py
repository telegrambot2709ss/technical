from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from django.utils.translation import gettext_lazy as _

from apps.api.v1.base.validate import validate_email
from apps.users.models import User, Sponsor


class UserSponsorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            validate_email,
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    fullname = serializers.CharField(max_length=100)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "fullname", "date_joined"]


class SponsorListCreateSerializer(serializers.ModelSerializer):
    user = UserSponsorSerializer(required=True)
    sponsor_type = serializers.CharField(max_length=15, required=True)
    summa = serializers.IntegerField(required=True)
    status = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        model = Sponsor
        fields = [
            "pk", "user", "sponsor_type", "status", "summa", "organization"
        ]

    def validate(self, attrs):
        if attrs['sponsor_type'] == Sponsor.SponsorType.LEGAL and not attrs.get('organization'):
            raise ValidationError({
                "sponsor_type": [_("The organization of the legal entity must be written!!!")]
            })
        if attrs['sponsor_type'] == Sponsor.SponsorType.PHYSICAL and attrs.get('organization'):
            raise ValidationError({
                "sponsor_type": [_("A natural person must not be an organization!!!")]
            })
        if attrs['summa'] == 0 or attrs['summa'] < 0:
            raise ValidationError({
                "summa": [_("Sponsorship must be greater than Zero!!!")]
            })
        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSponsorSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        sponsor = Sponsor.objects.create(user=user, **validated_data)
        return sponsor

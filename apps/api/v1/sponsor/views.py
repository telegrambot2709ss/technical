from rest_framework import generics
from rest_framework.filters import SearchFilter

from apps.api.v1.base.validate import validate_datetime
from apps.api.v1.base.pagination import CustomPagination
from apps.api.v1.base.permissions import IsAdminOrReadOnly
from apps.api.v1.sponsor import serializers
from apps.users.models import Sponsor


# Task 2
class SponsorListCreateView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorListCreateSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        'user__fullname', 'user__username', 'organization',
        'summa', 'user__date_joined__date', 'user__email'
    ]
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset

        date_from = validate_datetime(
            self.request.query_params.get('date_from')
        )
        date_to = validate_datetime(
            self.request.query_params.get('date_to')
        )
        fullname = self.request.query_params.get('fullname')
        status = self.request.query_params.get('status')
        summa = self.request.query_params.get('summa')

        if date_from and date_to:
            queryset = queryset.filter(user__date_joined__date__range=(date_from, date_to))
        if date_to and not date_from:
            queryset = queryset.filter(user__date_joined__date=date_to)
        if date_from and not date_to:
            queryset = queryset.filter(user__date_joined__date=date_from)
        if fullname:
            queryset = queryset.filter(user__fullname__contains=fullname)
        if status:
            queryset = queryset.filter(status=status)
        if summa and (type(summa) == int or summa.isdigit()):
            queryset = queryset.filter(summa=int(summa))

        return queryset

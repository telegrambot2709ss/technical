from collections import OrderedDict
from django.core.paginator import InvalidPage
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, replace_query_param, remove_query_param

from django.conf import settings

PER_PAGE = settings.PER_PAGE


class CustomPagination(PageNumberPagination):
    page_size = PER_PAGE
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def __init__(self):
        self.reverse = False
        self.request, self.paginator, self.page, self.count = None, None, None, 0

    def paginate_queryset(self, queryset, request, view=None):
        self.count = queryset.count()
        page_size = self.get_page_size(request)

        if not page_size:
            return None

        self.paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, self.paginator)
        try:
            self.page = self.paginator.page(page_number)
        except InvalidPage as exc:
            pass

        if self.paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page) if self.page else []

    def get_next_link(self):
        if not self.page or not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if self.count == 0:
            return None
        if not self.page:
            self.reverse = True
            self.page = self.paginator.page(self.paginator.num_pages)
            return self.get_previous_link()

        if not self.page.has_previous() and not self.reverse:
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number() if not self.reverse else self.paginator.num_pages
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

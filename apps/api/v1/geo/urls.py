from django.urls import path

from apps.api.v1.geo import views

urlpatterns = [
    path("region/list/", views.RegionListView.as_view(), name="region-list")
]

from django.urls import path

from apps.api.v1.thirdparty import views

urlpatterns = [
    path("weather/", views.ThirtyWeatherView.as_view(), name="thirty-party-weather"),
]

from django.urls import path

from apps.api.v1.sponsor import views

urlpatterns = [
    path('list/', views.SponsorListCreateView.as_view(), name='sponsor-list'),
    path('create/', views.SponsorListCreateView.as_view(), name='sponsor-create'),
]

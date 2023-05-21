from django.urls import path, include

from apps.api.v1.auth import urls as auth_urls
from apps.api.v1.sponsor import urls as sponsor_urls
from apps.api.v1.student import urls as student_urls
from apps.api.v1.files import urls as files_urls
from apps.api.v1.thirdparty import urls as thirty_party_urls
from apps.api.v1.geo import urls as geo_urls

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('sponsor/', include(sponsor_urls)),
    path('student/', include(student_urls)),
    path('file/', include(files_urls)),
    path('thirty/', include(thirty_party_urls)),
    path('geo/', include(geo_urls)),
]

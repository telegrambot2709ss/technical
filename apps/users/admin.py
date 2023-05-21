from django.contrib import admin
from apps.users.models import User, Sponsor, Student

admin.site.register(User)
admin.site.register(Sponsor)
admin.site.register(Student)

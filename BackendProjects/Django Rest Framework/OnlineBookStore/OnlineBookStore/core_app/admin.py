from django.contrib import admin
from django.apps import apps
from django.conf import settings


User = apps.get_model(settings.AUTH_USER_MODEL)
admin.site.register(User)

# Register your models here.

from django.contrib import admin
from apps.api.models import APINode

# Register your models here.
class api(admin.ModelAdmin):
    admin.site.register(APINode)
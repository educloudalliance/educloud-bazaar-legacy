from django.contrib import admin
from apps.library.models import ProductLibrary

# Register your models here.
class library(admin.ModelAdmin):
    admin.site.register(ProductLibrary)
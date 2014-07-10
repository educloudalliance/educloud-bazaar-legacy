from django.contrib import admin
from apps.api.models import MaterialItem, Tags, Comment, Ratings, ProviderOrganization, APINode
# Register your models here.
class api(admin.ModelAdmin):
    admin.site.register(MaterialItem)
    admin.site.register(Tags)
    admin.site.register(Comment)
    admin.site.register(Ratings)
    admin.site.register(ProviderOrganization)
    #admin.site.register(MaterialCollections)
    #admin.site.register(hasCollection)
    admin.site.register(APINode)
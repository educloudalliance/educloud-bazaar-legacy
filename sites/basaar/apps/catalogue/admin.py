from django.contrib import admin
from oscar.core.loading import get_model
from treebeard.admin import TreeAdmin

Tags = get_model('catalogue', 'Tags')
admin.site.register(Tags)

from django.contrib import admin
from oscar.core.loading import get_model
from treebeard.admin import TreeAdmin

Tags = get_model('catalogue', 'Tags')
Language = get_model('catalogue', 'Language')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')

admin.site.register(Language)
admin.site.register(EmbeddedMedia)
admin.site.register(Tags)

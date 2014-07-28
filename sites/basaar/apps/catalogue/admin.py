from django.contrib import admin
from oscar.core.loading import get_model
from treebeard.admin import TreeAdmin

Tags = get_model('catalogue', 'Tags')
Language = get_model('catalogue', 'Language')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')
Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductClass = get_model('catalogue', 'ProductClass')

admin.site.register(Language)
admin.site.register(EmbeddedMedia)
admin.site.register(Tags)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductClass)
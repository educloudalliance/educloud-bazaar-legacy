from django.db import models
from oscar.apps.catalogue.abstract_models import *

class Category(AbstractCategory):
    pass


class ProductClass(AbstractProductClass):
    pass


class Category(AbstractCategory):
    pass


class ProductCategory(AbstractProductCategory):
    pass


class Product(AbstractProduct):
    video_url = models.URLField(blank=True)
    materialUrl = models.URLField()
    iconUrl = models.URLField(blank=True)
    moreInfoUrl = models.URLField(blank=True)


class Tags(models.Model):
    name = models.CharField(max_length=128)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now_add=True)
    hasTags = models.ManyToManyField(Product)

    def __str__(self):
        return self.name



class ProductAttribute(AbstractProductAttribute):
    pass


class ProductAttributeValue(AbstractProductAttributeValue):
    pass


class AttributeOptionGroup(AbstractAttributeOptionGroup):
    pass


class AttributeOption(AbstractAttributeOption):
    pass


class AttributeEntity(AbstractAttributeEntity):
    pass


class AttributeEntityType(AbstractAttributeEntityType):
    pass


class Option(AbstractOption):
    pass


class ProductImage(AbstractProductImage):
    pass

from oscar.apps.catalogue.models import *
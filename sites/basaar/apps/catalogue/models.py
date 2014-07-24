from django.db import models
from oscar.apps.catalogue.abstract_models import *
from django.utils.translation import ugettext_lazy as _, pgettext_lazy


class Category(AbstractCategory):
    pass


class ProductClass(AbstractProductClass):
    pass



class ProductCategory(AbstractProductCategory):
    pass


class Product(AbstractProduct):
    uuid = models.CharField(max_length=50)
    materialUrl = models.URLField(blank=True)
    moreInfoUrl = models.URLField(blank=True)
    version = models.CharField(max_length=50)
    contributionDate = models.DateField(null=True)
    maxAge = models.IntegerField(null=True)
    minAge = models.IntegerField(null=True)
    contentLicense = models.CharField(max_length=4000)  #Apache limit from www.boutell.com/newfaq/misc/urllength.html
    dataLicense = models.CharField(max_length=4000)
    copyrightNotice = models.CharField(max_length=4000)
    attributionText = models.TextField()
    attributionURL = models.CharField(max_length=4000)

    def get_media(self):
        """
        Return a product's embedded media
        """
        url = []
        mediaArray = EmbeddedMedia.objects.filter(product=self)
        for media in mediaArray:
            url.append(media.url)

        return url

    get_media.short_description = _("Embedded media")

    def get_icon_url(self):
        filename = '/static/shop/img/icons/' + self.upc + '.png'
        return filename

class Language(models.Model):
    name = models.CharField(max_length=128)
    hasLanguage = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls):
        obj = cls()
        return obj


class EmbeddedMedia(models.Model):
    url = models.URLField(max_length=4000)
    product = models.ForeignKey(Product)

    def __str__(self):
        return self.url

    @classmethod
    def create(cls):
        obj = cls()
        return obj


class Tags(models.Model):
    name = models.CharField(max_length=128)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now_add=True)
    hasTags = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls):
        obj = cls()
        return obj



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
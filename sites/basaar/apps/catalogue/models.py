from django.db import models
import tempfile
import os
from oscar.apps.catalogue.abstract_models import *
from django.utils.translation import ugettext_lazy as _, pgettext_lazy


StockRecord = get_model('partner', 'StockRecord')


class Category(AbstractCategory):
    pass


class ProductClass(AbstractProductClass):
    pass


class ProductCategory(AbstractProductCategory):
    pass


class Product(AbstractProduct):
    uuid = models.CharField(max_length=50)
    materialUrl = models.URLField(blank=True)
    moreInfoUrl = models.URLField(blank=True, null=True)
    version = models.CharField(max_length=50)
    contributionDate = models.DateField(null=True)
    maximumAge = models.IntegerField(null=True)
    minimumAge = models.IntegerField(null=True)
    contentLicense = models.CharField(max_length=4000)  # Apache limit from www.boutell.com/newfaq/misc/urllength.html
    dataLicense = models.CharField(max_length=4000)
    copyrightNotice = models.CharField(max_length=4000)
    attributionText = models.TextField()
    attributionURL = models.CharField(max_length=4000)
    visible = models.BooleanField(default=False)
    iconUrl = models.URLField(null=True)
    upload_path = '/media/icons'
    icon = models.ImageField(upload_to=upload_path, null=True, blank=True)

    def saveIcon(self, *args, **kwargs):
        if self.iconUrl:
            import urllib2, os
            from urlparse import urlparse
            from PIL import Image, ImageChops
            try:
                req = urllib2.Request(self.iconUrl)
                response = urllib2.urlopen(req, None, 15)

                iconFile = self.upc + self.iconUrl[-4:]
                # TODO .jpeg?
                sPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
                filename = sPath + '/public/media/icons/' + iconFile
        
                f = tempfile.NamedTemporaryFile(delete=False)
                f.write(response.read())
                f.close()

                # Resize
                size = (200, 200)
                image = Image.open(f.name)
                image.thumbnail(size, Image.ANTIALIAS)
                image_size = image.size

                thumb = image.crop((0, 0, size[0], size[1]))
                offset_x = max((size[0] - image_size[0]) / 2, 0)
                offset_y = max((size[1] - image_size[1]) / 2, 0)

                thumb = ImageChops.offset(thumb, offset_x, offset_y)
                fileFolder = sPath + '/public/media/icons/'
                filename = self.upc + ".png"
                thumb.save(fileFolder + filename)
                print "Icon resized!"

                self.icon = os.path.join(self.upload_path, filename)
                super(Product, self).save()
                return True
            except Exception as e:
                print "Error on icon download: " + e.message
                return False


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
        if self.icon is not None:
            print self.icon

    def get_owner(self):
        product = StockRecord.objects.get(product=self)
        owner = product.partner

        return owner.name


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

    def __unicode__(self):
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
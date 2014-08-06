from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.api.models import APINode
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')
Tags = get_model('catalogue', 'Tags')
Language = get_model('catalogue', 'Language')
StockRecord = get_model('partner', 'StockRecord')
Category = get_model('catalogue', 'Category')
ProductCategory = get_model('catalogue', 'ProductCategory')
ProductClass = get_model('catalogue', 'ProductClass')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductClass
        fields = ('slug',)
        read_only_fields = ('slug',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    embedMedia = serializers.SerializerMethodField('mediaUrlLookup')
    tags = serializers.SerializerMethodField('tagsLookup')
    languages = serializers.SerializerMethodField('languageLookup')
    price = serializers.SerializerMethodField('priceLookup')
    subject = serializers.SerializerMethodField("subjectLookup")
    producttype = serializers.SerializerMethodField("productTypeLookup")

    def mediaUrlLookup(self, obj):
        objs = EmbeddedMedia.objects.filter(product=obj)
        #serializer = MediaUrlSerializer(objs, many=True)
        return objs #serializer.data

    def tagsLookup(self, obj):
        return Tags.objects.filter(hasTags=obj)

    def languageLookup(self, obj):
        return Language.objects.filter(hasLanguage=obj)

    def priceLookup(self, obj):
        return float(StockRecord.objects.get(product=obj).price_retail)

    def productTypeLookup(self, obj):
        return obj.product_class.slug

    def subjectLookup(self, obj):
        productCategories = ProductCategory.objects.filter(product=obj)
        categories = []
        for i in productCategories:
            categories.append(i.category.slug)
        return categories #productCategory.category.name


    class Meta:
        model = Product
        fields = ('uuid', 'title', 'description', 'materialUrl', 'moreInfoUrl', 'version',
        'contributionDate', 'maximumAge', 'minimumAge', 'contentLicense',
        'dataLicense', 'copyrightNotice', 'attributionText', 'attributionURL', 'embedMedia', 'tags', 'languages',
        'price', 'producttype', 'subject', 'visible', 'iconUrl')
        #read_only_fields = ('mTitle', 'slug')

class APINodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APINode
        fields = ('uniquePath', 'objectType')
        depth = 2


class MediaUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmbeddedMedia
        fields = ('url')

class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ('name')

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('name')

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockRecord
        fields = ('price_retail')

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        read_only_fields = ('name', 'slug',)
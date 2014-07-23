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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')



"""
class MaterialItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialItem
        fields = ('mTitle', 'description', 'materialUrl', 'materialType',
        'materialUrl', 'iconUrl', 'screenshotUrls', 'videoUrls', 'moreInfoUrl', 'bazaarUrl',
        'version', 'status', 'createdAt', 'price', 'language', 'issn')
        #read_only_fields = ('mTitle', 'slug')
"""

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    embedMedia = serializers.SerializerMethodField('mediaUrlLookup')
    tags = serializers.SerializerMethodField('tagsLookup')
    languages = serializers.SerializerMethodField('languageLookup')
    price = serializers.SerializerMethodField('priceLookup')
    subject = serializers.SerializerMethodField("subjectLookup")

    def mediaUrlLookup(self, obj):
        objs = EmbeddedMedia.objects.filter(product=obj)
        #serializer = MediaUrlSerializer(objs, many=True)
        return objs #serializer.data

    def tagsLookup(self, obj):
        return Tags.objects.filter(hasTags=obj)

    def languageLookup(self, obj):
        return Language.objects.filter(hasLanguage=obj)

    def priceLookup(self, obj):
        return StockRecord.objects.get(product=obj).price_retail

    def subjectLookup(self, obj):
        productCategory = ProductCategory.objects.get(product=obj)
        return productCategory.category.name


    class Meta:
        model = Product
        fields = ('uuid', 'title', 'description', 'materialUrl', 'moreInfoUrl', 'version',
        'contributionDate', 'maxAge', 'minAge', 'contentLicense',
        'dataLicense', 'copyrightNotice', 'attributionText', 'attributionURL', 'embedMedia', 'tags', 'languages', 'price', 'subject')
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
        fields = ('name')
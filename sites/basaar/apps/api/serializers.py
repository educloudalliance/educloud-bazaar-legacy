from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.api.models import APINode
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')

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
    class Meta:
        model = Product
        fields = ('uuid', 'title', 'description', 'materialUrl', 'iconUrl', 'moreInfoUrl', 'version',
        'price', 'contributionDate', 'maxAge', 'minAge', 'contentLicense',
        'dataLicense', 'copyrightNotice', 'attributionText', 'attributionURL',)
        #read_only_fields = ('mTitle', 'slug')

class APINodeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = APINode
        fields = ('uniquePath', 'objectType')
        depth = 2
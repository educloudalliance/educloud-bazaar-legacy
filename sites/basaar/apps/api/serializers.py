from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.api.models import MaterialCollections, MaterialItem

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialCollections
        fields = ('cTitle', 'slug',)
        read_only_fields = ('cTitle', 'slug')


class MaterialItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialItem
        fields = ('mTitle', 'slug', 'description', 'owner_org_name', 'license', 'free', 'link', 'itemType',
                    'createdAt', 'lastModified', 'numberOfRatings', 'numberOfLikes', )
        #read_only_fields = ('mTitle', 'slug')
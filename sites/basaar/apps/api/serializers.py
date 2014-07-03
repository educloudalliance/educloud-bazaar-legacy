from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.api.models import MaterialItem

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')




class MaterialItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialItem
        fields = ('mTitle', 'description', 'materialUrl', 'materialType',
        'materialUrl',)
        #read_only_fields = ('mTitle', 'slug')

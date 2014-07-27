from django.db import models
from django.contrib.auth.models import User, Group
from oscar.core.loading import get_class, get_model
import datetime
from autoslug import AutoSlugField
# Create your models here.

Product = get_model('catalogue', 'Product')

#this is a model which is used to describe the API-structure
class APINode(models.Model):
    uniquePath = models.CharField(max_length=8000)
    parentPath = models.CharField(max_length=8000, blank=True)
    objectType = models.CharField(max_length=20)
    materialItem = models.ForeignKey(Product, blank=True, null=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.uniquePath

    @classmethod
    def create(cls, uniqPath, parPath, objType):
        obj = cls(uniquePath=uniqPath, parentPath=parPath, objectType=objType)
        return obj




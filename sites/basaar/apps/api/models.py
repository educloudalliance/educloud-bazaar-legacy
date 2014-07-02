from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from autoslug import AutoSlugField
# Create your models here.

#Collection information is stored in this table
class MaterialCollections(models.Model):
    defaultValue = 1
    cTitle = models.CharField(max_length=255)
    createdAt =  models.DateTimeField(auto_now_add=True)
    lastModified = models.DateField(auto_now_add=True)
    createdBy = models.ForeignKey(User)
    uniqueTitle = models.CharField(max_length=8000)
    slug = AutoSlugField(populate_from='cTitle')

    def __str__(self):
        return self.cTitle

class hasCollection(models.Model):
    parentID = models.ForeignKey(MaterialCollections)
    childID = models.ForeignKey(MaterialCollections, related_name='child_id')

# fill in all the details we created for the API-definition
# and discuss the rating-thumb thing
class MaterialItem(models.Model):
    mTitle = models.CharField(max_length=255)
    description = models.TextField(max_length=8000)
    owner_org_name = models.CharField(max_length=255)   #this might be foreignkey
    license = models.CharField(max_length=255)
    free = models.BooleanField(default=True)
    link = models.TextField(max_length=8000)
    itemType = models.CharField(max_length=32)   # trial, full version
    createdAt =  models.DateTimeField(auto_now_add=True)
    lastModified = models.DateField(auto_now_add=True)
    numberOfRatings = models.IntegerField(default=0)
    numberOfLikes = models.IntegerField(default=0)
    collectionId= models.ForeignKey(MaterialCollections, default=MaterialCollections.defaultValue)
    author = models.ForeignKey(User)
    uniqueTitle = models.CharField(max_length=8000)
    slug = AutoSlugField(populate_from='mTitle')

    def __str__(self):
        return self.mTitle

    def getLikesOfItem(self):
        return self.numberOfLikes


# this is folksonomical tag right?
# needs modifications to be usable with Django's own user-system
class Tags(models.Model):
    name = models.CharField(max_length=128)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,related_name='user_id', default=1)
    lastModifiedBy = models.ForeignKey(User,related_name='modified_by_user_id', default=1)
    ItemTags = models.ManyToManyField(MaterialItem)

    def __str__(self):
        return self.Name


#class ItemTags(models.Model):
 #   itemId = models.ForeignKey(MaterialItem)
  #  tagsId = models.ForeignKey(Tags)


#note the separation of the comments and ratings:
class Ratings(models.Model):
    rate = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(User)

    def __str__(self):
        return self.Rate

class ItemRatings(models.Model):
    itemId = models.ForeignKey(MaterialItem)
    ratingsID = models.ForeignKey(Ratings)


class Comment(models.Model):
    commentText = models.TextField(max_length=8000)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.commentText

class ItemComments(models.Model):
    itemId = models.ForeignKey(MaterialItem)
    commentsID = models.ForeignKey(Comment)

#
class ProviderOrganization(models.Model):
    organizationName = models.CharField(max_length=2000)
    ownerUser = models.ForeignKey(User) #foreign key to the User (CMS user-account)

    def __str__(self):
        return self.organizationName

#connects the material to the owner organization
class ownerOfMaterial(models.Model):
    itemId = models.ForeignKey(MaterialItem)
    organizationId = models.ForeignKey(ProviderOrganization)

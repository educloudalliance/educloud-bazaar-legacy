from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db.models import Count
from rest_framework import viewsets
from apps.api.serializers import UserSerializer, GroupSerializer, CollectionSerializer, MaterialItemSerializer

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from apps.api import models
from django.http import Http404


# Create your views here.
# API-views
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# this view is used to handle all CMS interaction through collections
# and resources
class CMSView(APIView):
    permission_classes = (permissions.AllowAny,)    #TODO::CHANGE TO AUTHENTICATED LATER

    def splitUrl(self, url):
        splitpath = url.lower().split('/')
        splitpath = splitpath[3:]
        splitpath = filter(None,splitpath)
        return splitpath

    def isValidCompanyCollection(self, firstCollectionnameInUrl):
        try:
            tempCollObjects = models.MaterialCollections.objects.get(slug=firstCollectionnameInUrl)
        except models.MaterialCollections.DoesNotExist:
            return False
        return True

    #Get MaterialCollection Object
    def getMaterialCollectionObject(self, collectionToken):
        try:
            tempCollObject = models.MaterialCollections.objects.get(slug=collectionToken)
        except models.MaterialCollections.DoesNotExist:
            return Response('404 line 53')
        return tempCollObject

    #to get all collection objects
    def getMaterialCollectionObjects(self,collectionNameArray):
        tempCollections = []
        for eachToken in collectionNameArray:
            try:
                tempCollections.append(self.getMaterialCollectionObject(eachToken))
            except models.MaterialCollections.DoesNotExist:
                materialTokens.append(eachToken) #TODO:: replace this line with system exit
        return tempCollections
    #checks whether url has correct collection names or not and if item is specified then it is saved in materialTokens variable
    def isValidCollections(self, splitpath):
        tempmaterialTokens = []
        for eachToken in splitpath:
            try:
                temp = models.MaterialCollections.objects.get(slug=eachToken)
            except models.MaterialCollections.DoesNotExist:
                tempmaterialTokens.append(eachToken)
        return tempmaterialTokens

    #check if the last part of the url is the materialitem
    def isValidLastTokenAsItem(self,firstMaterialToken, lastUrlToken):
        if firstMaterialToken !=  lastUrlToken:
            return False
        return True

    #checks whether materialItemToken is present in materialItem table
    def isvalidMaterialItem(self,materialItemToken):
        try:
            materialItemObj = models.MaterialItem.objects.get(slug=materialItemToken)
            return True
        except models.MaterialItem.DoesNotExist:
            return False

    #returns the materialItem Object from DB
    def getMaterialItemObject(self,materialItemToken):
        try:
            materialItemObj = models.MaterialItem.objects.get(slug=materialItemToken)
            return materialItemObj
        except models.MaterialItem.DoesNotExist:
            return False #TODO :: replace with system exit functionality

    def isCollectionsInterconnected(self, collectionsArray):
         length = len(collectionsArray)-1
         for i in range(length):
            try:
                temp = models.hasCollection.objects.get(parentID=collectionsArray[i].id, childID=collectionsArray[i+1].id)
            except models.hasCollection.DoesNotExist:
                return False
         return True

    #finds the children of the given collection
    def findCollectionChildren(self, collection):
        try:
            children = models.MaterialItem.objects.get(collectionId=collection)
            return children
        except models.MaterialItem.DoesNotExist:
            return []

    #finds the subcollections of the collection:
    def findSubcollections(self, collection):
        try:
            hasColl = models.hasCollection.objects.filter(parentID=collection)
            subColls = []
            for i in range(0, hasColl.count()):
                try:
                    subColls.append( models.MaterialCollections.objects.filter(pk=hasColl[i].childID))
                except models.MaterialCollections.DoesNotExist:
                    pass
            return subColls
        except models.hasCollection.DoesNotExist:
            return []


    def get(self, request):
        #get the collection and resource names from url:
        splitpath = self.splitUrl(request.path)
        materialTokens = []
        leftoverTokens=[]
        tempCollections = []
        jsonResponseStr = []
        length = 0
        successFlag = ''

        successFlag = self.isValidCompanyCollection(splitpath[0])
        if not successFlag:
            return Response('404 line 91')

        tempCollObj = self.getMaterialCollectionObject(splitpath[0])

        try:
            firstToken = models.hasCollection.objects.get(childID=tempCollObj.id)
            return Response('404 line 97')
        except models.hasCollection.DoesNotExist:

            materialTokens = self.isValidCollections(splitpath)
            #more than one materialitem is specified in url then error is returned
            if len(materialTokens) >1:
                return Response('404 line 103')

            #there is one materialitem in the url
            if len(materialTokens) == 1:
                #check if the last part of the url is the materialitem
                successFlag = self.isValidLastTokenAsItem(materialTokens[0],splitpath[len(splitpath)-1])
                if not successFlag :
                    return Response('404 line 110')

                #check whether Material Item exists or not
                successFlag = self.isvalidMaterialItem(materialTokens[0])
                if not successFlag :
                    return Response('404 line 114')
                else:
                    materialItemObj = self.getMaterialItemObject(materialTokens[0])
                #get all materialCollection objects
                tempCollections = self.getMaterialCollectionObjects(splitpath[:-1])

                serializer = MaterialItemSerializer(materialItemObj, many=False)
                #check all collections are interconnected if more than one collection is specified
                if len(tempCollections) >1:
                    length =len(tempCollections)-1
                    #checking collections are interconnected
                    successFlag = self.isCollectionsInterconnected(tempCollections)
                    if not successFlag:
                        return Response('404 line 153')


                    #check if the materialitem is connected to the last collection
                    if materialItemObj.collectionId.id == tempCollections[length].id:
                        jsonResponseStr.append(serializer.data)
                    else:
                        return Response('404')

                #if only one collection is present then check it is connected with item
                elif len(tempCollections) ==1:
                   if materialItemObj.collectionId.id != tempCollections[0].id:
                       return Response('404')
                   else:
                       jsonResponseStr.append(serializer.data)

            else:
                #if there is no materialitems, we should still return collection information
                # so we get all materialCollection objects

                tempCollections = self.getMaterialCollectionObjects(splitpath)
                children = self.findSubcollections(tempCollections[-1])


                serializer = CollectionSerializer(children, many=False)
                return Response(serializer.data)
                
                if len(tempCollections) >1:
                    length =len(tempCollections)-1
                    #check if the collections are connected to each other
                    successFlag = self.isCollectionsInterconnected(tempCollections)
                    if not successFlag:
                        return Response('404 line 179')

                    jsonResponseStr.append(serializer.data)
                elif len(tempCollections) ==1:
                    length =1
                    jsonResponseStr.append(serializer.data) #tempCollections[0].cTitle + " collection")

        return Response(jsonResponseStr)
        #raise Http404

    def post(self,request):
        splitpath = self.splitUrl(request.path)
        materialTokens = []
        leftoverTokens=[]
        tempCollections = []
        jsonResponseStr = []
        length = 0

        tempCollObj = self.isValidCompanyCollection(splitpath)

        try:
            firstToken = models.hasCollection.objects.get(childID=tempCollObj.id)
            return Response('404 line 155')
        except models.hasCollection.DoesNotExist:
            materialTokens = self.isValidCollections(splitpath)






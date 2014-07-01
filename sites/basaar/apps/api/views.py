from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apps.api.serializers import UserSerializer, GroupSerializer
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
    permission_classes = (permissions.AllowAny,)    #CHANGE TO AUTHENTICATED LATER

    def splitUrl(self, url):
        splitpath = url.split('/')
        splitpath = splitpath[3:]
        splitpath = filter(None,splitpath)
        return splitpath

    def isValidCompanyCollection(self, splitpath):
        try:
            tempCollObjects = models.MaterialCollections.objects.get(slug=splitpath[0])
        except models.MaterialCollections.DoesNotExist:
            return Response('404 line 54')
        return tempCollObjects

    #checks whether url has correct collection names or not and if item is specified then it is saved in materialTokens variable
    def isValidCollections(self, splitpath):
        tempmaterialTokens = []
        for eachToken in splitpath:
            try:
                temp = models.MaterialCollections.objects.get(slug=eachToken)
            except models.MaterialCollections.DoesNotExist:
                tempmaterialTokens.append(eachToken)
        #more than one materialitem is specified in url then error is returned
        if len(tempmaterialTokens) >1:
            return Response('404 line 68')
        return tempmaterialTokens

    def get(self, request, cmsurl):
        #get the collection and resource names from url:
        splitpath = self.splitUrl(request.path)
        materialTokens = []
        leftoverTokens=[]
        tempCollections = []
        jsonResponseStr = []
        length = 0

        tempCollObj = self.isValidCompanyCollection(splitpath)

        try:
            firstToken = models.hasCollection.objects.get(childID=tempCollObj.id)
            return Response('404 line 56')
        except models.hasCollection.DoesNotExist:
            materialTokens = self.isValidCollections(splitpath)

            #there is one materialitem in the url
            if len(materialTokens) ==1:
                lefttokens = materialTokens

                #check if the last part of the url is the materialitem
                if materialTokens[0] !=  splitpath[len(splitpath)-1]:
                    return Response('404')

                try:
                    materialItemObj = models.MaterialItem.objects.get(slug=materialTokens[0])
                except models.MaterialItem.DoesNotExist:
                    return Response('404')

                #to get all collection objects
                for eachToken in splitpath[:-1]:
                    try:
                        tempCollections.append(models.MaterialCollections.objects.get(slug=eachToken))
                    except models.MaterialCollections.DoesNotExist:
                        materialTokens.append(eachToken)

                #check all collections are interconnected if more than one collection is specified
                if len(tempCollections) >1:
                    length =len(tempCollections)-1
                    for i in range(length):
                        try:
                            temp = models.hasCollection.objects.get(parentID=tempCollections[i].id, childID=tempCollections[i+1].id)
                        except models.hasCollection.DoesNotExist:
                            return Response('404')

                    #check if the materialitem is connected to the last collection
                    if materialItemObj.collectionId.id == tempCollections[length].id:
                        jsonResponseStr.append(materialItemObj.mTitle + "  " + materialItemObj.description +"  " + materialItemObj.itemType)
                    else:
                        return Response('404')

                #if only one collection is present then check it is connected with item
                elif len(tempCollections) ==1:
                   if materialItemObj.collectionId.id != tempCollections[0].id:
                       return Response('404')
                   else:
                       jsonResponseStr.append(materialItemObj.mTitle + "  " + materialItemObj.description + "  " +materialItemObj.itemType)

            else:
                #if there is no materialitems, we should still return collection information
                for eachToken in splitpath:
                    try:
                        tempCollections.append(models.MaterialCollections.objects.get(slug=eachToken))
                    except models.MaterialCollections.DoesNotExist:
                        materialTokens.append(eachToken)

                if len(tempCollections) >1:
                    length =len(tempCollections)-1

                    #check if the collections are connected to each other
                    for i in range(length):
                        try:
                            temp = models.hasCollection.objects.get(parentID=tempCollections[i].id, childID=tempCollections[i+1].id)
                        except models.hasCollection.DoesNotExist:
                            return Response('404')
                    jsonResponseStr.append(tempCollections[length].cTitle + " collection")
                elif len(tempCollections) ==1:
                    length =1
                    jsonResponseStr.append(tempCollections[0].cTitle + " collection")

        return Response(jsonResponseStr)
        #raise Http404

    def post(self,request, cmsurl):
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
            





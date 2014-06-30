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
    def get(self, request, cmsurl):
        #get the collection and resource names from url:
        splitpath = request.path.split('/')
        splitpath = splitpath[3:]
        splitpath = filter(None,splitpath)
        tempTokens = []
        leftoverTokens=[]
        tempCollections = []
        jsonResponseStr = []
        length = 0

        tempCollObj = models.MaterialCollections.objects.get(slug=splitpath[0])
        try:
            firstToken = models.hasCollection.objects.get(childID=tempCollObj.id)
            if firstToken:
                return Response('404')
        except models.hasCollection.DoesNotExist:
            #checks whether url has correct collection names or not and if item is specfied then it is saved in leftovertokens variable
            for eachToken in splitpath:
                try:
                    temp = models.MaterialCollections.objects.get(slug=eachToken)
                except models.MaterialCollections.DoesNotExist:
                    tempTokens.append(eachToken)

            #more than one item is specified in url then error is returned
            if len(tempTokens) >1:
                return Response('404')

            if len(tempTokens) ==1:
                lefttokens = tempTokens
                if tempTokens[0] !=  splitpath[len(splitpath)-1]:
                    return Response('404')

                for eachToken in lefttokens:
                    try:
                        tempItemObj = models.MaterialItem.objects.get(slug=eachToken)

                    except models.MaterialItem.DoesNotExist:
                        leftoverTokens.append(eachToken)

                if len(leftoverTokens) >0:
                    return Response('404')
                #to get all collection objects
                for eachToken in splitpath[:-1]:
                    try:
                        tempCollections.append(models.MaterialCollections.objects.get(slug=eachToken))
                    except models.MaterialCollections.DoesNotExist:
                        tempTokens.append(eachToken)

                #check all collections are interconnected if more than one collection is specified
                if len(tempCollections) >1:
                    length =len(tempCollections)-1
                    for i in range(length):
                        try:
                            temp = models.hasCollection.objects.get(parentID=tempCollections[i].id, childID=tempCollections[i+1].id)
                        except models.hasCollection.DoesNotExist:
                            return Response('404')

                    if tempItemObj.collectionId.id == tempCollections[length].id:
                        jsonResponseStr.append(tempItemObj.mTitle + "  " + tempItemObj.description +"  " + tempItemObj.itemType)
                    else:
                        return Response('404')
                 #if only one collection is present then check it is connected with item
                elif len(tempCollections) ==1:
                   if tempItemObj.collectionId.id != tempCollections[0].id:
                       return Response('404')
                   else:
                       jsonResponseStr.append(tempItemObj.mTitle + "  " + tempItemObj.description + "  " +tempItemObj.itemType)

            else:
                for eachToken in splitpath:
                    try:
                        tempCollections.append(models.MaterialCollections.objects.get(slug=eachToken))
                    except models.MaterialCollections.DoesNotExist:
                        tempTokens.append(eachToken)

                if len(tempCollections) >1:
                    length =len(tempCollections)-1
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





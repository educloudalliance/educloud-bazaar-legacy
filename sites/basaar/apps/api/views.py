from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db.models import Count
from rest_framework import viewsets
from apps.api.serializers import UserSerializer, GroupSerializer, MaterialItemSerializer

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from apps.api import models
import json
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
        splitpath = splitpath[0:]
        splitpath = filter(None,splitpath)
        return splitpath

    def checkIfAlreadyInDb(self, path):
        return models.APIObject.objects.filter(uniquePath=path).exists()

    #make sure there isn't items in the middle of the given path
    def checkIfItemsInPostPath(self, path):
        urlTokens = self.splitUrl(path)
        pathSoFar = "" #urlTokens[0]
        for i in range(0, len(urlTokens)):

            if models.APIObject.objects.filter(uniquePath=pathSoFar, objectType="item").exists():
                #we found an object which is an item and in middle of the given path.
                #because items can't have children, this is an ERROR condition.
                return True
            else:
                pathSoFar += "/" + urlTokens[i]

    #after we have verified that the url can be used to create new item or collection, check
    #the path and list not existing collections to be created.
    #If collection exists already, nothing happens.
    def createCollections(self, path):
        urlTokens = self.splitUrl(path)
        parentPathSoFar = ""
        pathSoFar = urlTokens[0]
        createdCollection = []
        for i in range(1, len(urlTokens)+1):
            if models.APIObject.objects.filter(uniquePath=pathSoFar, objectType="collection").exists():
                #the collection exists, therefore it doesn't need to be created.
                parentPathSoFar = pathSoFar
                if i < len(urlTokens):
                    pathSoFar += "/" + urlTokens[i] #move to the next
            else:
                #the collection doesn't exist yet so create it:
                newColl = models.APIObject.create(pathSoFar, parentPathSoFar, "collection")
                newColl.save()
                parentPathSoFar = pathSoFar
                createdCollection.append(pathSoFar)

                if i < len(urlTokens):
                    pathSoFar += "/" + urlTokens[i] #move to the next

        return "Created collections: " + str(createdCollection)


    def postMaterialItem(self, path, data):
        #entries = []
        #entries.append(data)
        #take json-array of the pushes and take the forces:

        theList = data["items"]
        names = ""
        for x in theList:
            #create new item
            item = models.MaterialItem.create()
            item.save()


            names += x["title"]


        return names

    def get(self, request):
        return Response('WORK IN PROGRESS')

    def post(self,request):
        url = request.path
        url = url[len("/api/cms/"):] #slice the useless part away
        #return Response(str(type(request.DATA["title"])))
        #return Response(request.DATA)
        #check if the object exists in the db already:
        if self.checkIfAlreadyInDb(url):
            return Response("ERROR: Can't post because an object already exists in this URL. " + url)

        if self.checkIfItemsInPostPath(url):
            return Response("ERROR: There is an item in middle of the path. Item's can't have children.")

        #create collections if needed
        createdCollections = self.createCollections(url)

        #try to create a new item:
        createdItems = self.postMaterialItem(url, request.DATA)

        return Response(createdCollections + " --- " + createdItems)


        """splitpath = self.splitUrl(request.path)
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
            materialTokens = self.isValidCollections(splitpath)"""






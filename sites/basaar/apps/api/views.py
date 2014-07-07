from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db.models import Count
from rest_framework import viewsets
from apps.api.serializers import UserSerializer, GroupSerializer, MaterialItemSerializer, APIObjectSerializer

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from apps.api import models
from datetime import datetime
import json
from django.template.defaultfilters import slugify

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

        for x in range(0, len(splitpath)):
            splitpath[x] = slugify(splitpath[x])    #remove bad characters from url
        return splitpath

    def slugifyWholeUrl(self, url):
        urlarray = self.splitUrl(url)
        url= urlarray[0]
        for i in range(1, len(urlarray)):
            url += "/" + urlarray[i]

        return url

    def checkIfAlreadyInDb(self, path):
        return models.APIObject.objects.filter(uniquePath=self.slugifyWholeUrl(path)).exists()

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
        theList = data["items"]
        createdItems = []
        #TODO: WRITE A PROPER SERIALIZER FOR THIS!!!!!!!!!!!!!!!!!
        for x in theList:
            #create new item
            item = models.MaterialItem.create()
            item.mTitle = x["title"]
            item.description = x["description"]
            item.materialUrl = x["materialUrl"]
            item.materialType = x["materialType"]
            item.iconUrl = x["iconUrl"]
            item.moreInfoUrl = x["moreInfoUrl"]
            item.bazaarUrl = x["bazaarUrl"]         #TODO: THIS IS PROBLEMATIC
            item.version = x["version"]
            item.status = x["status"]
            item.price = x["price"]
            item.language = x["language"]
            item.issn = x["issn"]
            item.author = User.objects.get(username="admin")    #TODO: User should be set to authenticated user when authentication is done

            try:
                item.createdAt = datetime.strptime(x["creationDate"], "%Y-%m-%d")
            except ValueError:
                #item.delete()
                return "Items created: " + createdItems + " ERROR: Creationdate field was in wrong format. Should be yyyy-mm-dd"

            #note that these are PickleFields which include arrays of strings.
            item.screenshotUrls = x["screenshotUrls"]
            item.videoUrls = x["videoUrls"]
            #TODO: TAGS ARE STILL MISSING


            if self.checkIfAlreadyInDb(path + "/" + slugify(item.mTitle)):
                return "ERROR: Can't post because an object already exists in this URL. Items created: " + unicode(createdItems)
            createdItems.append(item.mTitle)
            item.save()

            #add APIObject for this materialItem
            finalUrl = path + "/" + slugify(item.mTitle)
            newColl = models.APIObject.create(finalUrl, path, "item")
            newColl.materialItem = item
            newColl.save()


        return "Items created: " + unicode(createdItems)

    def get(self, request):
        url = request.path
        url = url[len("/api/cms/"):] #slice the useless part away
        #slice the trailing:
        url = url.strip("/")

        try:
            target = models.APIObject.objects.get(uniquePath=url)

            #check is the APIObject collection or item:
            if target.objectType == "item":
                #return JSON data of the materialItem:
                serializer = MaterialItemSerializer(target.materialItem)
                return Response(serializer.data)
            else:
                #find objects in this collection
                children = models.APIObject.objects.filter(parentPath=target.uniquePath)
                serializer = APIObjectSerializer(children, many=True)
                return Response(serializer.data)


        except models.APIObject.DoesNotExist:
            return Response("404: No such collection or materialItem.")











    def post(self,request):
        url = request.path
        url = url[len("/api/cms/"):] #slice the useless part away
        #return Response(str(type(request.DATA["title"])))
        #return Response(request.DATA)
        #check if the object exists in the db already:


        if self.checkIfItemsInPostPath(url):
            return Response("ERROR: There is an item in middle of the path. Item's can't have children.")

        #create collections if needed
        createdCollections = self.createCollections(url)

        #try to create a new item:
        createdItems = self.postMaterialItem(url, request.DATA)

        return Response(createdCollections + " --- " + createdItems)








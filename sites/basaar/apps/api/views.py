import urllib2, os, sys
from PIL import Image, ImageChops
from django.views.decorators.csrf import csrf_exempt
import uuid as libuuid
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db.models import Count
from rest_framework import viewsets
from apps.api.serializers import UserSerializer, GroupSerializer, APINodeSerializer, ProductSerializer, ProductTypeSerializer, SubjectSerializer
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
#from apps.catalogue import models as catalogueModels
from oscar.core.loading import get_class, get_model
from apps.api import models
from datetime import datetime
import json
from django.template.defaultfilters import slugify
from rest_framework import authentication, permissions
from rest_framework.authentication import OAuth2Authentication, BasicAuthentication, SessionAuthentication
from apps.api.permissions import IsOwner
from rest_framework import generics

from django.http import Http404


Product = get_model('catalogue', 'Product')
ProductCategory = get_model('catalogue', 'ProductCategory')
Language = get_model('catalogue', 'Language')
Tag = get_model('catalogue', 'Tags')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')
Category = get_model('catalogue', 'Category')
ProductClass = get_model('catalogue', 'ProductClass')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')

class AuthException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return repr("Authorization error")

class RootException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return repr("Cannot create Root-nodes")

class DataException(Exception):
    msg = ""
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


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



class ProductTypeList(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows productType's to be viewed.
    """
    queryset = ProductClass.objects.all()
    serializer_class = ProductTypeSerializer
    paginate_by = 100

class SubjectList(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subject's to be viewed.
    """
    queryset = Category.objects.all()
    serializer_class = SubjectSerializer
    paginate_by = 100


# this view is used to handle all CMS interaction through collections
# and resources
class CMSView(APIView):
    """
    Returns a list of all items and collections in the provided collection in url if url
    points to a valid collection or item. In case of collections a json list of items and collections
    is returned while in case of a materialitem a json representation of the material is returned.
    """
    #authentication_classes = (OAuth2Authentication, BasicAuthentication, SessionAuthentication)
    #permission_classes = ( IsOwner, ) #permissions.IsAuthenticatedOrReadOnly,
    authentication_classes = (OAuth2Authentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)

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

    #check whether there is empty strings in the url
    def isValidUrl(self,path):
        splitpath = self.trimTheUrl(path)
        print splitpath
        if len(splitpath) == 0:
            return False
        return True

    #trim unnecessary part of url
    def trimTheUrl(self,path):
        url = path
        url = url[len("/api/cms/"):] #slice the useless part away
        #slice the trailing:
        url = url.strip("/")

        return url

    def checkIfAlreadyInDb(self, path):
        return models.APINode.objects.filter(uniquePath=self.slugifyWholeUrl(path)).exists()

    #make sure there isn't items in the middle of the given path
    def checkIfItemsInPostPath(self, path):
        urlTokens = self.splitUrl(path)
        pathSoFar = "" #urlTokens[0]
        for i in range(0, len(urlTokens)):
            print pathSoFar
            pathSoFar = pathSoFar.strip("/")
            if models.APINode.objects.filter(uniquePath=pathSoFar, objectType="item").exists():
                #we found an object which is an item and in middle of the given path.
                #because items can't have children, this is an ERROR condition.
                return True
            else:
                pathSoFar += "/" + urlTokens[i]

        if models.APINode.objects.filter(uniquePath=pathSoFar, objectType="item").exists():
            #we found an object which is an item and in middle of the given path.
            #because items can't have children, this is an ERROR condition.
            return True

        print "Lopuksi: " + pathSoFar
        return False


    #after we have verified that the url can be used to create new item or collection, check
    #the path and list not existing collections to be created.
    #If collection exists already, nothing happens.
    def createCollections(self, path, request):
        urlTokens = self.splitUrl(path)
        parentPathSoFar = ""
        pathSoFar = urlTokens[0]
        createdCollection = []

        #check if the first collection exists. If not, throw exception:
        if models.APINode.objects.filter(uniquePath=pathSoFar, objectType="collection").exists() == False:
            raise RootException()

        for i in range(1, len(urlTokens)+1):

            try:
                node = models.APINode.objects.get(uniquePath=pathSoFar, objectType="collection")
                #if models.APINode.objects.filter(uniquePath=pathSoFar, objectType="collection").exists():

                perm = IsOwner()
                if not perm.has_object_permission(request, self, node):
                    raise AuthException()

                #the collection exists, therefore it doesn't need to be created.
                parentPathSoFar = pathSoFar
                if i < len(urlTokens):
                    pathSoFar += "/" + urlTokens[i] #move to the next

            except models.APINode.DoesNotExist:
                #the collection doesn't exist yet so create it:
                newColl = models.APINode.create(pathSoFar, parentPathSoFar, "collection")
                newColl.owner = request.user
                newColl.save()
                parentPathSoFar = pathSoFar
                createdCollection.append(pathSoFar)

                if i < len(urlTokens):
                    pathSoFar += "/" + urlTokens[i] #move to the next

        return "Created collections: " + str(createdCollection)

    #check whether json has items or not
    def checkJsonData(self,request):
        theList = request.DATA
        if len(theList) == 0:
            return False
        try:
            theItems = request.DATA["items"]
        except:
            return  False
        return True

    def postMaterialItem(self, path, request):
        theList = request.DATA["items"]
        createdItems = []


        #TODO: WRITE A PROPER SERIALIZER FOR THIS!!!!!!!!!!!!!!!!!
        for x in theList:
            #Add product into database
            try:
                itemClass = ProductClass.objects.get(name=x["productType"])
            #TODO Create better error handling
            except:
                return "Product Class cannot be found"

            #Create unique UPC
            createdUPC = self.createUPC()

            #TODO: Make a proper serializer
            #TODO: subject=x["subject"]
            product = Product(title=x["title"], upc=createdUPC, description=x["description"], materialUrl=x["materialUrl"],
                              moreInfoUrl=x["moreInfoUrl"],  uuid=x["uuid"], version=x["version"],
                              maxAge=x["maximumAge"], minAge=x["minimumAge"], contentLicense=x["contentLicense"],
                              dataLicense=x["dataLicense"], copyrightNotice=x["copyrightNotice"], attributionText=x["attributionText"],
                              attributionURL=x["attributionURL"], product_class=itemClass)    #TODO: product_class on product type

            #Add fullfilment into database
            author = Partner.objects.get(name=self.splitUrl(path)[0])

            try:
                product.contributionDate = datetime.strptime(x["contributionDate"], "%Y-%m-%d")
            except ValueError:
                return "Items created: " + createdItems + " ERROR: ContributionDate field was in wrong format. Should be yyyy-mm-dd"

            if self.checkIfAlreadyInDb(path + "/" + slugify(product.uuid)):
                return "ERROR: Can't post because an object already exists in this URL. Items created: " + unicode(createdItems)

            createdItems.append(product.title)

            #Download icon
            if x["iconUrl"] is not None:
                self.downloadIcon(x["iconUrl"], createdUPC)

            product.save()

            if Category.objects.filter(slug=x["subject"]).exists():
                    category = Category.objects.get(slug=x["subject"])
                    newProductCategory = ProductCategory(product=product, category=category)
                    newProductCategory.save()
            else:
                product.delete()
                return "No such product category as in subject field: " + x["subject"]


            #create language, Tags and EmbeddedMedia models
            langList = x["language"]
            for lan in langList:
                print lan
                #check if the language is already in db, if not create it
                if Language.objects.filter(name=lan).exists():
                    l = Language.objects.get(name=lan)
                    l.hasLanguage.add(product)
                else:
                    langEntry = Language.create()
                    langEntry.name = lan
                    langEntry.save()
                    langEntry.hasLanguage.add(product)

            #tags creation
            tagList = x["tags"]

            if len(tagList) > 5:
                raise DataException("Error: More than 5 tags specified. Only 0-5 allowed.")

            for tag in tagList:
                print tag
                #check if the tag is already in db, if not create it
                if Tag.objects.filter(name=tag).exists():
                    t = Tag.objects.get(name=tag)
                    t.hasTags.add(product)
                else:
                    tagEntry = Tag.create()
                    tagEntry.name = tag
                    tagEntry.save()
                    tagEntry.hasTags.add(product)

            #oEmbed
            embedList = x["embedMedia"]
            for media in embedList:
                print media
                embedEntry = EmbeddedMedia.create()
                embedEntry.url = media
                embedEntry.product = product
                embedEntry.save()

            f = StockRecord(product=product, partner=author, price_excl_tax=x["price"], price_retail=x["price"], partner_sku=x["uuid"])
            f.save()

            #add APINode for this materialItem
            finalUrl = path + "/" + slugify(product.uuid)
            newColl = models.APINode.create(finalUrl, path, "item")
            newColl.materialItem = product
            newColl.owner = request.user
            newColl.save()


        return "Items created: " + unicode(createdItems)


    def get(self, request):

        isValid = self.isValidUrl(request.path)
        if not isValid:
            return Response("Error: The url is empty.")

        url = self.trimTheUrl(request.path)
        print url

        try:
            target = models.APINode.objects.get(uniquePath=url)
            perm = IsOwner()
            perm.has_object_permission(request, self, target)
            #check is the APINode collection or item:
            if target.objectType == "item":
                #return JSON data of the materialItem:
                serializer = ProductSerializer(target.materialItem)
                return Response(serializer.data)
            else:
                #find objects in this collection
                children = models.APINode.objects.filter(parentPath=target.uniquePath)
                serializer = APINodeSerializer(children, many=True)
                return Response(serializer.data)

        except models.APINode.DoesNotExist:
            return Response("404: No such collection or materialItem.")


    @csrf_exempt
    def post(self,request):
        isValid = self.isValidUrl(request.path)
        if not isValid:
            return Response("Error: The url is empty")

        if not self.checkJsonData(request):
            return Response("No JSON data available")

        url = self.trimTheUrl(request.path)
        print url

        #check if the object exists in the db already:
        url = self.slugifyWholeUrl(url)

        if self.checkIfItemsInPostPath(url):
            return Response("ERROR: There is an item in middle of the path. Item's can't have children.")

        #create collections if needed
        try:
            try:
                createdCollections = self.createCollections(url, request)
            except RootException:
                return Response("ERROR: Can't create new root nodes.")
        except AuthException:
            return Response("ERROR: You are not the owner of a node in path.")

        #try to create a new item:
        #TODO: Put a string describing the field with error to the thrown error to be shown
        try:
            createdItems = self.postMaterialItem(url, request)
        except IntegrityError:
            return Response("ERROR: There is already a resource with same uuid. uuid must be unique.")
        except KeyError:
            return Response("Error: Missing or invalid json-field. Update failed.")
            #except ValueError:
            #    return Response("Error: ContributionDate field was in wrong format. Should be yyyy-mm-dd")
            #except TypeError:
            #return Response("Error: ContributionDate field was in wrong format. Should be yyyy-mm-dd")
        except DataException as e:
            return Response(e.msg)

        return Response(createdCollections + " --- " + createdItems)


    def put(self,request):
        inValidItemsNames = ""
        isValid = self.isValidUrl(request.path)
        if not isValid:
            return Response("Error: The url is empty.")
        url = self.trimTheUrl(request.path)
        print url

        #if not self.checkJsonData(request):
        #    return Response("No JSON data available")

        if models.APINode.objects.filter(uniquePath=url).exists():
            node = models.APINode.objects.get(uniquePath=url)
            if node.objectType == "item":
                target = node.materialItem
                try:
                    self.updateExistingItem(target, request.DATA)
                except KeyError:
                    return Response("Error: Missing or invalid json-field. Update failed.")
                except ValueError:
                    return Response("Error: ContributionDate field was in wrong format. Should be yyyy-mm-dd")
                except DataException as e:
                    return Response(e.msg)

                return Response("Material item at " + url +" updated successfully.")
            else:
                return Response("Target is not an item but a collection.")
        else:
            return Response("No such item in db to update. ")



    #updates an existing Product with data provided in the request
    def updateExistingItem(self,obj, DATA):
        obj.title = DATA["title"]
        obj.description = DATA["description"]
        obj.materialUrl = DATA["materialUrl"]
        obj.version = DATA["version"]
        obj.contributionDate = datetime.strptime(DATA["contributionDate"], "%Y-%m-%d")
        obj.moreInfoUrl = DATA["moreInfoUrl"]
        obj.maxAge = DATA["maximumAge"]
        obj.minAge = DATA["minimumAge"]
        obj.contentLicense = DATA["contentLicense"]
        obj.dataLicense = DATA["dataLicense"]
        obj.copyrightNotice = DATA["copyrightNotice"]
        obj.attributionText = DATA["attributionText"]
        obj.attributionURL = DATA["attributionURL"]

        #update subject
        if Category.objects.filter(slug=DATA["subject"]).exists():
            category = Category.objects.get(slug=DATA["subject"])
            productCategory = ProductCategory.objects.get(product=obj)    #ProductCategory(product=product, category=category)
            productCategory.category = category
            productCategory.save()
        else:
            raise DataException("No such product category as in subject field: " + DATA["subject"])

        stock = StockRecord.objects.get(product=obj)
        stock.price_retail = DATA["price"]
        stock.save()

        tagList = DATA["tags"]
        #Remove existing relationships to this material from tags
        existingTags = Tag.objects.filter(hasTags=obj)
        for t in existingTags:
            print "Remove tag reference"
            t.hasTags.remove(obj)

        for tag in tagList:
            print tag
            #check if the tag is already in db, if not create it
            if Tag.objects.filter(name=tag).exists():
                t = Tag.objects.get(name=tag)
                t.hasTags.add(obj)
            else:
                tagEntry = Tag.create()
                tagEntry.name = tag
                tagEntry.save()
                tagEntry.hasTags.add(obj)

        #oEmbed
        embedList = DATA["embedMedia"]
        #remove existing embed urls
        existing = EmbeddedMedia.objects.filter(product=obj)
        for e in existing:
            e.delete()

        #create new ones
        for media in embedList:
            print media
            embedEntry = EmbeddedMedia.create()
            embedEntry.url = media
            embedEntry.product = obj
            embedEntry.save()


        #Remove existing relationships to this material from languages
        langList = DATA["language"]
        existingLangs = Language.objects.filter(hasLanguage=obj)
        for l in existingLangs:
            print "Remove language reference"
            l.hasLanguage.remove(obj)

        for lang in langList:
            #check if the language is already in db, if not create it
            if Language.objects.filter(name=lang).exists():
                    l = Language.objects.get(name=lang)
                    l.hasLanguage.add(obj)
            else:
                langEntry = Language.create()
                langEntry.name = lang
                langEntry.save()
                langEntry.hasLanguage.add(obj)


        obj.save()

    """
    def delete(self,request):
        inValidItemsNames = ""
        isValid = self.isValidUrl(request.path)
        if not isValid:
            return Response("Error: The url is empty.")
        url = self.trimTheUrl(request.path)
        #print url

        if not self.checkJsonData(request):
            return Response("No JSON data available")

        theList = request.DATA["items"]
        inValidItems = []
        for eachItem in theList:
            finalUrl = url + "/" + slugify(eachItem["title"])
            if not models.APINode.objects.filter(uniquePath=finalUrl).exists():
                inValidItems.append(eachItem["title"])
            else:
                self.deleteExisitingItem(finalUrl,eachItem)

        if len(inValidItems) == 0:
            return Response("Successfully deleted data")
        else:
            for eachItem in inValidItems:
                inValidItemsNames += eachItem
                inValidItemsNames += ",  "
            return Response("items not found:"+inValidItemsNames)
    """
    def deleteExisitingItem(self,finalUrl,x):
        itemNode = models.APINode.objects.get(uniquePath=finalUrl)
        itemNode.materialItem.delete()
        itemNode.delete()
        #item.delete()
        #itemNode.delete()

    #Download icon into static folder
    def downloadIcon(self, url, iconName):
        #TODO Image resizing
        allowedMimes = ['image/gif', 'image/jpeg', 'image/png']

        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req, None, 15)

            #Get headers
            headers = response.info()

            if headers['content-type'] in allowedMimes:
                iconFile = iconName + url[-4:]
                #TODO .jpeg?
                sPath = os.path.dirname(sys.argv[0])
                filename = sPath + '/' + 'static/shop/img/icons/' + iconFile
                output = open(filename, 'wb')
                output.write(response.read())
                output.close()

                # Resize
                size = (200, 200)
                image = Image.open(filename)
                image.thumbnail(size, Image.ANTIALIAS)
                image_size = image.size

                thumb = image.crop( (0, 0, size[0], size[1]) )
                offset_x = max( (size[0] - image_size[0]) / 2, 0 )
                offset_y = max( (size[1] - image_size[1]) / 2, 0 )

                thumb = ImageChops.offset(thumb, offset_x, offset_y)
                filename = sPath + '/' + 'static/shop/img/icons/' + iconName + ".png"
                thumb.save(filename)
                print "Icon resized!"
            else:
                return False

        except urllib2.URLError, e:
            #TODO better error handling
            if e == 404:
                #TODO return 404 error ?
                return False
            else:
                return False
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
            return False
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False


    #Create unique UPC for material
    def createUPC(self):
        UPC = str(libuuid.uuid4())
        UPC = UPC.replace("-", "")
        UPC = UPC[0:10]

        while models.Product.objects.filter(upc=UPC).exists():
            UPC = str(libuuid.uuid4())
            UPC = UPC.replace("-", "")
            UPC = UPC[0:15]

        return UPC

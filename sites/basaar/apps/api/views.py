import urllib2, os, sys
from PIL import Image, ImageChops
from django.views.decorators.csrf import csrf_exempt
import uuid as libuuid
from rest_framework.renderers import UnicodeJSONRenderer
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
from rest_framework import permissions
from django.http import Http404
from errorcodes import *

Product = get_model('catalogue', 'Product')
ProductCategory = get_model('catalogue', 'ProductCategory')
Language = get_model('catalogue', 'Language')
Tag = get_model('catalogue', 'Tags')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')
Category = get_model('catalogue', 'Category')
ProductClass = get_model('catalogue', 'ProductClass')
Partner = get_model('partner', 'Partner')
StockRecord = get_model('partner', 'StockRecord')

#success messages:
postSuccess = {"message" : "Operation successful, created: "}
putSuccess = {"message" : "Operation successful, updated "}

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class SubjectList(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subject's to be viewed.
    """
    queryset = Category.objects.all()
    serializer_class = SubjectSerializer
    paginate_by = 100
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# this view is used to handle all CMS interaction through collections
# and resources
class CMSView(APIView):
    """
    Returns a list of all items and collections in the provided collection in url if url
    points to a valid collection or item. In case of collections a json list of items and collections
    is returned while in case of a materialitem a json representation of the material is returned.

    """
    #authentication_classes = (OAuth2Authentication, BasicAuthentication, SessionAuthentication)
    #renderer_classes = (UnicodeJSONRenderer,)
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
            raise UrlIsEmpty()


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
            raise RootError()

        for i in range(1, len(urlTokens)+1):

            try:
                node = models.APINode.objects.get(uniquePath=pathSoFar, objectType="collection")
                perm = IsOwner()
                if not perm.has_object_permission(request, self, node):
                    raise AuthError()

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

        return unicode(createdCollection)


    def str2Bool(self, s, fieldName):
        if s == "false":
            return False
        elif s == "true":
            return True
        else:
            raise IncorrectBooleanField(fieldName)


    #check whether json has items or not
    def checkJsonData(self,request):
        theList = request.DATA
        if len(theList) == 0:
            raise NoJSON()
        try:
            theItems = request.DATA["items"]
        except:
            raise NoJSON()


    def postMaterialItem(self, path, request):
        theList = request.DATA["items"]
        createdApiNodes = []
        createdProducts = []
        createdStockRecords = []

        try:
            #TODO: WRITE A PROPER SERIALIZER FOR THIS!!!!!!!!!!!!!!!!!
            for x in theList:
                #Add product into database
                try:
                    itemClass = ProductClass.objects.get(slug=x["productType"])
                #TODO Create better error handling
                except:
                    raise ProductTypeNotFound(x["productType"]) #RollbackException("Error: Product class with type " + x["productType"] + " could not be found.")

                #Create unique UPC
                createdUPC = self.createUPC()

                #check optional fields
                if "moreInfoUrl" in x:
                    moreInfoUrl = x["moreInfoUrl"]
                else:
                    moreInfoUrl = None

                visible = self.str2Bool(x["visible"], "visible")
                product = Product(title=x["title"], upc=createdUPC, description=x["description"], materialUrl=x["materialUrl"],
                                  moreInfoUrl=moreInfoUrl,  uuid=x["uuid"], version=x["version"],
                                  maximumAge=x["maximumAge"], minimumAge=x["minimumAge"], contentLicense=x["contentLicense"],
                                  dataLicense=x["dataLicense"], copyrightNotice=x["copyrightNotice"], attributionText=x["attributionText"],
                                  attributionURL=x["attributionURL"],visible=visible, product_class=itemClass)    #TODO: product_class on product type

                #Add fullfilment into database
                author = Partner.objects.get(code=self.splitUrl(path)[0])

                if "contributionDate" in x:
                    try:
                        product.contributionDate = datetime.strptime(x["contributionDate"], "%Y-%m-%d")
                    except ValueError:
                        raise InvalidDate()
                else:
                    product.contributionDate = None

                if self.checkIfAlreadyInDb(path + "/" + slugify(product.uuid)):
                    raise ObjectAlreadyExists( path + "/" + slugify(product.uuid) )

                #Download icon if one is specified
                if "iconUrl" in x is not None:
                    self.downloadIcon(x["iconUrl"], createdUPC)
                    print "tallenna urli"
                    product.iconUrl = x["iconUrl"]

                product.save()
                createdProducts.append(product)

                #find subjects:
                subs = x["subjects"]
                if len(subs) == 0:
                    raise WrongAmountOfSubjects()
                if len(subs) > 5:
                    raise WrongAmountOfSubjects()

                for subject in subs:
                    if subs.count(subject) > 1:
                        raise EachSubjectOnlyOnce()

                for subject in subs:
                    if Category.objects.filter(slug=subject).exists():
                            category = Category.objects.get(slug=subject)
                            newProductCategory = ProductCategory(product=product, category=category)
                            newProductCategory.save()
                    else:
                        raise SubjectNotFound(subject)



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
                if "tags" in x:
                    tagList = x["tags"]

                    if len(tagList) > 5:
                        raise TooMuchTags()

                    for tag in tagList:
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
                if "embedMedia" in x:
                    embedList = x["embedMedia"]
                    for media in embedList:
                        print media
                        embedEntry = EmbeddedMedia.create()
                        embedEntry.url = media
                        embedEntry.product = product
                        embedEntry.save()

                f = StockRecord(product=product, partner=author, price_excl_tax=x["price"], price_retail=x["price"], partner_sku=x["uuid"], num_in_stock=1)
                f.save()
                createdStockRecords.append(f)


                #add APINode for this materialItem
                finalUrl = path + "/" + slugify(product.uuid)
                newColl = models.APINode.create(finalUrl, path, "item")
                newColl.materialItem = product
                newColl.owner = request.user
                newColl.save()
                createdApiNodes.append(newColl)

        except RollbackException as e:
            self.doRollback(createdApiNodes, createdProducts, createdStockRecords)
            raise RollbackException(e.msg + " All changes/materialItems canceled.")
        except Exception, e:
            #Rollback the process because of an other error
            self.doRollback(createdApiNodes, createdProducts, createdStockRecords)
            raise e

        success = ""
        for i in createdApiNodes:
            success += i.uniquePath + " , "
        return success

    #this function cancels all the operations done in post if there is an exception
    def doRollback(self, createdApiNodes, createdProducts, createdStockRecords):
        for node in createdApiNodes:
            node.delete()

        for product in createdProducts:
            self.unlinkTags(product)
            self.unlinkSubjects(product)
            self.unlinkLanguages(product)
            self.removeoEmbeds(product)
            product.delete()

        for stock in createdStockRecords:
            stock.delete()


    def get(self, request):

        try:
            isValid = self.isValidUrl(request.path)

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
                raise ObjectNotFound(url)

        except RollbackException as e:
            return Response(e.msg)


    @csrf_exempt
    def post(self,request):

        try:
            self.isValidUrl(request.path)
            self.checkJsonData(request)

            url = self.trimTheUrl(request.path)

            #check if the object exists in the db already:
            url = self.slugifyWholeUrl(url)

            if self.checkIfItemsInPostPath(url):
                raise ItemOnPath()

            #create collections if needed
            self.createCollections(url, request)

            #try to create a new item:
            try:
                createdItems = self.postMaterialItem(url, request)
            #except IntegrityError:
            #    return Response("ERROR: There is already a resource with same uuid. uuid must be unique.")
            except KeyError as e:
                raise MissingField(e.message)
                #except ValueError:
                #    return Response("Error: ContributionDate field was in wrong format. Should be yyyy-mm-dd")
                #except TypeError:
                #return Response("Error: ContributionDate field was in wrong format. Should be yyyy-mm-dd")

        except RollbackException as e:
            return Response(e.getDict(), status=e.httpStatus)

        msg = postSuccess.copy()
        msg["message"] += createdItems
        return Response(msg)


    def put(self,request):
        try:
            self.isValidUrl(request.path)
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
                    except KeyError as e:
                        raise MissingField(e.message)

                    msg = putSuccess.copy()
                    msg["message"] += url
                    return Response(msg)
                else:
                    raise CantUpdateCollection()
            else:
                raise ObjectNotFound(url)

        except RollbackException as e:
            return Response(e.getDict(), status=e.httpStatus)


    #updates an existing Product with data provided in the request
    def updateExistingItem(self,obj, DATA):
        obj.title = DATA["title"]
        obj.description = DATA["description"]
        obj.materialUrl = DATA["materialUrl"]
        obj.version = DATA["version"]

        visible = self.str2Bool(DATA["visible"], "visible")
        obj.visible = visible

        try:
            itemClass = ProductClass.objects.get(slug=DATA["productType"])
            obj.product_class = itemClass
        except ProductClass.DoesNotExist:
            raise ProductTypeNotFound(DATA["productType"])

        if "contributionDate" in DATA:
            try:
                obj.contributionDate = datetime.strptime(DATA["contributionDate"], "%Y-%m-%d")
            except ValueError:
                raise InvalidDate()
        else:
            obj.contributionDate = None

        if "moreInfoUrl" in DATA:
            obj.moreInfoUrl = DATA["moreInfoUrl"]
        else:
            obj.moreInfoUrl = None

        obj.maximumAge = DATA["maximumAge"]
        obj.minimumAge = DATA["minimumAge"]
        obj.contentLicense = DATA["contentLicense"]
        obj.dataLicense = DATA["dataLicense"]
        obj.copyrightNotice = DATA["copyrightNotice"]
        obj.attributionText = DATA["attributionText"]
        obj.attributionURL = DATA["attributionURL"]

        #update subject
        subs = DATA["subjects"]
        if len(subs) == 0:
            raise WrongAmountOfSubjects()
        if len(subs) > 5:
            raise WrongAmountOfSubjects()
        for subject in subs:
            if subs.count(subject) > 1:
                raise EachSubjectOnlyOnce()

        #check if the given subjects are valid ones
        for subject in subs:
            if not Category.objects.filter(slug=subject).exists():
                raise SubjectNotFound(subject)

        #remove existing subject links
        self.unlinkSubjects(obj)

        #create new ones
        for subject in subs:
            category = Category.objects.get(slug=subject)
            newProductCategory = ProductCategory(product=obj, category=category)
            newProductCategory.save()

        stock = StockRecord.objects.get(product=obj)
        stock.price_retail = DATA["price"]
        stock.save()

        #Remove existing relationships to this material from tags
        self.unlinkTags(obj)

        if "tags" in DATA:
            tagList = DATA["tags"]

            if len(tagList) > 5:
                raise TooMuchTags()

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
        #remove existing embed urls
        self.removeoEmbeds(obj)

        if "embedMedia" in DATA:
            embedList = DATA["embedMedia"]
            #create new ones
            for media in embedList:
                embedEntry = EmbeddedMedia.create()
                embedEntry.url = media
                embedEntry.product = obj
                embedEntry.save()


        #Remove existing relationships to this material from languages
        self.unlinkLanguages(obj)
        langList = DATA["language"]

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

        if "iconUrl" in DATA and DATA["iconUrl"] is not None:
            self.downloadIcon(DATA["iconUrl"], obj.upc)
            obj.iconUrl = DATA["iconUrl"]
        obj.save()

    def removeoEmbeds(self, product):
        existing = EmbeddedMedia.objects.filter(product=product)
        for e in existing:
            e.delete()

    def unlinkTags(self, product):
        existingTags = Tag.objects.filter(hasTags=product)
        for t in existingTags:
            t.hasTags.remove(product)

    def unlinkSubjects(self, product):
        #remove existing subject links
        oldPCategs = ProductCategory.objects.filter(product=product)
        for pc in oldPCategs:
            pc.delete()

    def unlinkLanguages(self, product):
        existingLangs = Language.objects.filter(hasLanguage=product)
        for l in existingLangs:
            l.hasLanguage.remove(product)

    #Download icon into static folder
    def downloadIcon(self, url, iconName):
        #TODO Image resizing
        allowedMimes = ['image/gif', 'image/jpeg', 'image/png']

        try:
            print "Icon requested from " + url
            req = urllib2.Request(url)
            response = urllib2.urlopen(req, None, 15)

            #Get headers
            headers = response.info()

            if headers['Content-Type'] in allowedMimes and int(headers['Content-Length']) < 10000000:
                iconFile = iconName + url[-4:]

                #TODO .jpeg?
                sPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))
                filename = sPath + '/public/static/shop/img/icons/' + iconFile
                print "orig:" + filename
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
                filename = sPath + '/' + '/public/static/shop/img/icons/' + iconName + ".png"
                print "thumb:" + filename
                thumb.save(filename)
                print "Icon resized!"
            else:
                print headers['Content-Length']
                print "Not allowed MIME or image too big"
                return False

        except urllib2.URLError, e:
            #TODO better error handling
            if e == 404:
                print "404 on icon download"
                #TODO return 404 error ?
                return False
            else:
                print "HTTP-error on icon download"
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

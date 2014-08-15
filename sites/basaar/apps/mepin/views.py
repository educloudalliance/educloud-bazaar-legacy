from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from oscar.core.loading import get_class, get_model
from django.http import Http404
import requests
import json
# Create your views here.

def index(request):
   # if not request.user.is_authenticated():
    #    raise PermissionDenied()

   # user = User.objects.get(username=request.user.username)
   # try:
     #   userPartner = Partner.objects.get(users=user)
   # except Partner.DoesNotExist:
    #   raise PermissionDenied()

   # ids = StockRecord.objects.values_list('product', flat=True).filter(partner=userPartner)
   # productList = Product.objects.filter(pk__in=set(ids)
    token = request.GET.get('access_token')

    payload = {'access_token' : token}

    mepin_auth_url = "https://0933e43ceeeb3a21de15489b7057f686c998a3dccdf8c88e9769484eaad31e99:5aedf3cb23a908d430724c502a64a0275d7e7a75635b8275e9b5771eb2c3d2cfe0326202ea8fb8b209c86a7537fcf3d07bf48c8e190ce6bfd3e4fd7060ab20cc@api.mepin.com/simple_api/user_info"

    mepin_response = requests.post(mepin_auth_url,data=payload,verify=False)

    try:
        parseJsonResponse = json.loads(mepin_response.text)
        ID = parseJsonResponse['mepin_id']
        print User.objects.filter(email = ID).exists()

        if not User.objects.filter(email = ID).exists():
           cuser = User.objects.create_user(ID,ID,'mepin')
           cuser.set_password('mepin')
           cuser.save()

        getusername = User.objects.get(email = ID)
        print (getusername.username + '  heloooooooooo')
        user = authenticate(username=getusername.username,password ='mepin')
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                ID = 'account disabled contact administrator'
        else:
            ID = 'Invalid login'

    except:
        print 'error 404'
        #raise Http404
    template = loader.get_template('catalogue/browse.html')
    context = RequestContext(request, {

    })
    #return HttpResponse(template.render(context))
    return HttpResponseRedirect("/catalogue/")

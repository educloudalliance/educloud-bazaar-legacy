from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
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
        User = get_user_model()
        print User.objects.filter(mepinId = ID).exists()
        print ID
        if not User.objects.filter(mepinId = ID).exists():
           #cuser = User.objects.create_user(ID, 'a@a.com')
           #cuser.set_password('mepin')
           #cuser.mepinId=ID
           #cuser.username=ID
           #cuser.save()
           cuser = User.create()
           cuser.username = ID
           cuser.email = ID + '@mepin.com'
           cuser.set_password('mepin')
           cuser.mepinId = ID
           cuser.save()

        getusername = User.objects.get(mepinId = ID)
        redirecttoprofile = True
        cemail = getusername.email
        findstring = '@mepin.com'
        print findstring in cemail
        if not findstring in cemail:
            redirecttoprofile = False
        print (getusername.username + '  heloooooooooo')
        #user = authenticate(username=getusername.username,password =getusername.password)
        #print authenticate(username=ID,password ='mepin')
        getusername.backend = 'django.contrib.auth.backends.ModelBackend'
        if getusername is not None:
            if getusername.is_active:
                login(request, getusername)
            else:
                ID = 'account disabled contact administrator'
        else:
            ID = 'Invalid login'

    except Exception as e:
        print e
        raise Http404
    template = loader.get_template('catalogue/browse.html')
    context = RequestContext(request, {
    })
    print redirecttoprofile
    #return HttpResponse(template.render(context))
    if redirecttoprofile == True:
        return HttpResponseRedirect("/accounts/profile/edit")
    else:
        return HttpResponseRedirect("/catalogue/")

